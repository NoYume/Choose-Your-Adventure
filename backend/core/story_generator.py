from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode
from core.models import StoryLLMResponse, StoryNodeLLM

load_dotenv()

class StoryGenerator:
    
    @classmethod
    def _get_llm(cls):
        anthropic_api_key = os.getenv("CHOREO_ANTHROPIC_CONNECTION_ANTHROPIC_API_KEY")
        serviceurl = os.getenv("CHOREO_ANTHROPIC_CONNECTION_SERVICEURL")
        
        if anthropic_api_key and serviceurl:
            return ChatAnthropic(model="claude-3-haiku-20240307", api_key=anthropic_api_key, base_url=serviceurl)
        
        return ChatAnthropic(model="claude-3-haiku-20240307")
    
    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy")-> Story:
        llm = cls._get_llm()
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                STORY_PROMPT
            ),
            (
                "human",
                f"Create the story with this theme: {theme}"
            )
        ]).partial(format_instructions=story_parser.get_format_instructions())

        raw_response = llm.invoke(prompt.invoke({}))

        response_text = raw_response
        if hasattr(raw_response, "content"):
            response_text = raw_response.content

        story_structure = story_parser.parse(response_text)

        story_db = Story(title=story_structure.title, session_id=session_id)
        db.add(story_db)
        db.flush()

        root_node_data = story_structure.rootNode
        if isinstance(root_node_data, dict):
            root_node_data = StoryNodeLLM.model_validate(root_node_data)

        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)

        db.commit()
        return story_db
    
    
    @classmethod
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False) -> StoryNode:
        if hasattr(node_data, "content"):
            content = node_data.content
        else:
            content = node_data.get("content")
        
        if hasattr(node_data, "isEnding"):
            is_ending = node_data.isEnding
        else:
            is_ending = node_data.get("isEnding", False)
        
        if hasattr(node_data, "isWinningEnding"):
            is_winning_ending = node_data.isWinningEnding
        else:
            is_winning_ending = node_data.get("isWinningEnding", False)
        
        node = StoryNode(
            story_id=story_id,
            content=content,
            is_root=is_root,
            is_ending=is_ending,
            is_winning_ending=is_winning_ending,
            options=[]
        )
        db.add(node)
        db.flush()

        has_options = False
        options_data = []
        
        if hasattr(node_data, "options") and node_data.options:
            options_data = node_data.options
            has_options = True
        elif isinstance(node_data, dict) and node_data.get("options"):
            options_data = node_data["options"]
            has_options = True

        if not node.is_ending and has_options:
            options_list = []
            
            for option_data in options_data:
                if not option_data:
                    continue
                    
                option_text = None
                if hasattr(option_data, "text"):
                    option_text = option_data.text
                elif isinstance(option_data, dict) and "text" in option_data:
                    option_text = option_data["text"]
                
                next_node = None
                if hasattr(option_data, "nextNode"):
                    next_node = option_data.nextNode
                elif isinstance(option_data, dict) and "nextNode" in option_data:
                    next_node = option_data["nextNode"]
                
                if not option_text or not next_node:
                    continue

                if isinstance(next_node, dict):
                    if "isEnding" not in next_node:
                        next_node["isEnding"] = False
                    if "isWinningEnding" not in next_node:
                        next_node["isWinningEnding"] = False
                    if "content" not in next_node:
                        continue
                        
                    try:
                        next_node = StoryNodeLLM.model_validate(next_node)
                    except Exception:
                        continue

                try:
                    child_node = cls._process_story_node(db, story_id, next_node, False)
                    
                    options_list.append({
                        "text": option_text,
                        "node_id": child_node.id
                    })
                except Exception:
                    continue

            node.options = options_list

        db.flush()
        return node