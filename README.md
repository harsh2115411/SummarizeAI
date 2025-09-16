# 🦜 AI YouTube Video Summarizer
## 🚀 Live Demo: [Click Here](https://summarizeai-24nwkijyszxyi9q3gur9ak.streamlit.app/)

A powerful Streamlit web application that automatically extracts and summarizes YouTube video content using advanced AI technology. Get concise, meaningful summaries of any YouTube video in seconds!

## ✨ Features

- **🎯 Smart Summarization**: Uses Groq's LLaMA-3.1-8b-instant model for high-quality summaries
- **📝 Transcript Extraction**: Automatically extracts video transcripts using YouTube Transcript API
- **🔄 Map-Reduce Processing**: Handles long videos efficiently by chunking and combining summaries
- **💾 Session Management**: Maintains your summaries and URLs across sessions
- **🎨 User-Friendly Interface**: Clean, intuitive Streamlit interface
- **⚡ Fast Processing**: Quick turnaround for most video lengths

## 🚀 Demo

Simply paste any YouTube URL and click "Summarize" to get:
- A concise 300-word summary
- Key points and main ideas from the video
- Persistent results that stay until you clear them

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Groq API key

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/youtube-summarizer.git
cd youtube-summarizer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up your Groq API key**
   - Get your API key from [Groq Console](https://console.groq.com/)
   - Create a `.streamlit/secrets.toml` file:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

4. **Run the application**
```bash
streamlit run app.py
```

## 📦 Dependencies

```
streamlit
langchain
langchain-groq
langchain-community
validators
youtube-transcript-api
yt-dlp
```

## 🎯 Usage

1. **Launch the app**: Run `streamlit run app.py`
2. **Enter YouTube URL**: Paste any YouTube video URL in the input field
3. **Click Summarize**: Hit the "Summarize the Content from YT or Website" button
4. **Get Results**: Receive a comprehensive summary in ~300 words
5. **Clear Results**: Use the "Clear" button to reset for a new video

### Supported URL Formats
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`

## ⚙️ How It Works

1. **URL Validation**: Checks if the provided URL is a valid YouTube link
2. **Transcript Extraction**: Uses YouTube Transcript API to fetch video transcripts
3. **Text Chunking**: Splits long transcripts into manageable chunks (2000 chars with 200 overlap)
4. **Map-Reduce Summarization**: 
   - **Map Phase**: Creates 150-word summaries for each chunk
   - **Reduce Phase**: Combines partial summaries into a final 300-word summary
5. **Display Results**: Shows the final summary with session persistence

## 🚨 Important Notes

- **Content Restrictions**: Some YouTube videos may not work due to transcript availability or channel restrictions
- **Processing Time**: Large videos may take longer to process
- **Rate Limits**: Your IP may get blocked by YouTube if you make too many requests quickly
- **API Costs**: Groq API usage may incur costs based on your plan

## 🔧 Configuration

### Customizing Summary Length
You can modify the prompt templates in the code:

```python
# For individual chunk summaries (default: 150 words)
map_prompt_template = """
Summarize the following content in 150 words:
{text}
"""

# For final combined summary (default: 300 words)
combine_prompt_template = """
You are given multiple partial summaries. 
Combine them into a single clear summary in about 300 words:
{text}
"""
```

### Changing Model
To use a different Groq model, modify:
```python
llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=groq_api_key)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web app framework
- [LangChain](https://python.langchain.com/) for the powerful AI orchestration
- [Groq](https://groq.com/) for fast AI inference
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api) for transcript extraction

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Ensure your Groq API key is properly configured

---

**⭐ If you find this project helpful, please give it a star!**
