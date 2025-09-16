import validators, streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
from langchain.schema import Document
from langchain_community.document_loaders import WebBaseLoader

# --- Streamlit UI ---
st.set_page_config(page_title="LangChain: Summarize Text From YT, Webpage", page_icon="🦜")
st.title("🦜 SUMMARIZE AI ")
st.subheader('Summarize URL or Youtube video')
st.sidebar.title("Imprtant Information")
st.sidebar.info("Some web url and Youtube videos may not work due to restrictions on extracting content. In that case if error occurs, please try with another url or video.")
st.sidebar.info("Large videos or web pages may take longer time to process.")

# --- API Key Input ---
groq_api_key = st.secrets["GROQ_API_KEY"]

# --- Session State ---
if "summary" not in st.session_state:
    st.session_state["summary"] = ""
if "url" not in st.session_state:
    st.session_state["url"] = ""

# --- Input field with session state ---
generic_url = st.text_input("URL", value=st.session_state["url"], label_visibility="collapsed")


# --- LLM Setup ---
llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=groq_api_key)

# --- Prompt ---
map_prompt_template = """
Summarize the following content in 150 words:
{text}
"""
map_prompt = PromptTemplate(template=map_prompt_template, input_variables=["text"])

combine_prompt_template = """
You are given multiple partial summaries. 
Combine them into a single clear summary in about 300 words:
{text}
"""
combine_prompt = PromptTemplate(template=combine_prompt_template, input_variables=["text"])

if st.button("Summarize the Content from YT or Website"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL. It can be a YT video or website URL")
    else:
        try:
            with st.spinner("Processing..."):
                # --- Load data ---
                if "youtube.com" in generic_url:
                    parsed_url = urlparse(generic_url)
                    if "youtube" in parsed_url.netloc:
                        query_params = parse_qs(parsed_url.query)
                        if "v" in query_params:
                            video_id = query_params["v"][0]
                        else:
                            video_id = parsed_url.path.split("/")[-1]
                    elif "youtu.be" in parsed_url.netloc:
                        video_id = parsed_url.path.lstrip("/")
                    else:
                        st.error("Invalid YouTube URL")
                    try:
                        ytt_api = YouTubeTranscriptApi()
                        result = ytt_api.fetch(video_id)
                        text = " ".join(snippet.text for snippet in result.snippets)
                        if text.strip():
                            docs = [Document(page_content=text, metadata={"source": generic_url})]
                    except Exception as e:
                        st.warning(f"YouTubeTranscriptApi failed: {e}")       
                    
                else:
                    loader = WebBaseLoader(generic_url)
                    docs = loader.load()
                 
                # --- Split large documents ---
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1500,
                    chunk_overlap=200
                )
                split_docs = text_splitter.split_documents(docs)

                # --- Map Reduce Summarization ---
                chain = load_summarize_chain(
                    llm,
                    chain_type="map_reduce",
                    map_prompt=map_prompt,
                    combine_prompt=combine_prompt
                )
                output_summary = chain.run(split_docs)

                # --- Save to session state ---
                st.session_state["summary"] = output_summary
                st.session_state["url"] = generic_url

        except Exception as e:
            st.exception(f"Exception: {e}")

# --- Show summary if available ---
if st.session_state["summary"]:
    st.success(st.session_state["summary"])

# --- Clear Button ---
if st.button("Clear"):
    st.session_state["summary"] = ""
    st.session_state["url"] = ""   # clears the input box
    st.rerun()
