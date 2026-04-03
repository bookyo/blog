# 7 LangChain Code Examples That Make Building AI Apps Actually Simple

LangChain has become the go-to framework for building LLM-powered applications. But between chains, agents, and RAG pipelines, the learning curve can feel steep. That's where working code examples save hours of debugging.

Here are **7 LangChain examples** that cover the most important patterns — from basic chains to production-ready RAG systems. All free, all runnable.

---

## 1. LangChain Fundamentals — Prompt Templates & Basic Chains

Most AI apps start with the same problem: how do you inject dynamic data into an LLM prompt without writing spaghetti code?

LangChain's **PromptTemplate** solves this cleanly.

```python
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI

# Simple prompt template with dynamic variables
template = """You are a {role} assistant.
The user's question is: {question}
Provide a clear, concise answer in {tone} tone."""

prompt = PromptTemplate(
    input_variables=["role", "question", "tone"],
    template=template
)

chain = LLMChain(llm=OpenAI(temperature=0.7), prompt=prompt)

response = chain.run({
    "role": "Python tutor",
    "question": "What is a decorator?",
    "tone": "beginner-friendly"
})
print(response)
```

The magic here is **variable injection**. You define placeholders once, pass data at runtime. No string concatenation, no formatting bugs.

Want to chain multiple steps? Use `SequentialChain`:

```python
from langchain.chains import SequentialChain

# Chain 1: Generate outline
outline_chain = LLMChain(
    llm=OpenAI(),
    prompt=PromptTemplate(
        input_variables=["topic"],
        template="Give a 5-point outline for: {topic}"
    )
)

# Chain 2: Expand each point
expand_chain = LLMChain(
    llm=OpenAI(),
    prompt=PromptTemplate(
        input_variables=["outline"],
        template="Expand this outline into paragraphs:\n{outline}"
    )
)

# Run both in sequence
full_chain = SequentialChain(chains=[outline_chain, expand_chain])
result = full_chain.run({"topic": "How blockchain works"})
```

This means you can break complex tasks into digestible steps, each handled by a specialized prompt.

**[Try it live →](https://elysiatools.com/en/samples/langchain)**

---

## 2. Conversation Memory — Give Your AI a Brain

Stateless LLMs forget everything after each call. That's fine for one-shot tasks, but terrible for chatbots and assistants.

LangChain's **ConversationBufferMemory** solves this:

```python
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI

memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm=OpenAI(),
    memory=memory,
    verbose=True
)

# First exchange
conversation.run("My name is Alice and I work at Stripe.")

# Second exchange — AI remembers Alice and Stripe
response = conversation.run("What company do I work at?")
print(response)  # "You work at Stripe!"
```

For long conversations, use `ConversationBufferWindowMemory` to only keep the last *N* exchanges — prevents context window overflow while maintaining relevance.

```python
from langchain.memory import ConversationBufferWindowMemory

# Keep only last 5 exchanges
short_memory = ConversationBufferWindowMemory(k=5)
```

This means you can build ChatGPT-style bots with genuine short-term memory in under 20 lines of code.

**[Try it live →](https://elysiatools.com/en/samples/langchain)**

---

## 3. Building Agents — LLMs That Take Actions

Agents are where LangChain gets genuinely exciting. An **agent** isn't just a prompt — it's an LLM that decides *what tools to use* to answer your question.

```python
from langchain.agents import load_tools, initialize_agent
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory

# Load built-in tools
tools = load_tools(["serpapi", "llm-math"], llm=OpenAI())

# Create agent with a conversational memory
memory = ConversationBufferMemory(memory_key="chat_history")
agent = initialize_agent(
    tools,
    OpenAI(),
    agent="conversational-react-description",
    memory=memory,
    verbose=True
)

# Ask a question that requires web search + calculation
agent.run(
    "Who is the CEO of OpenAI and what is their age divided by 2?"
)
```

The agent autonomously decides to:
1. Search the web for the CEO's name
2. Search for their age
3. Use the calculator tool to divide by 2

No hardcoded flows. The LLM figures out the plan.

**[Try it live →](https://elysiatools.com/en/samples/langchain)**

---

## 4. Custom Tools — Connect Any API or Function

Built-in tools are great, but real apps need your own business logic. Define custom tools in seconds:

```python
from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from datetime import datetime

def get_current_time(format="%H:%M:%S"):
    """Returns the current time in HH:MM:SS format"""
    return datetime.now().strftime(format)

# Wrap as a LangChain tool
time_tool = Tool(
    name="CurrentTime",
    func=get_current_time,
    description="Returns the current time. Input is the time format string (default: %H:%M:%S)."
)

# Combine with other tools
tools = [time_tool]
agent = initialize_agent(tools, OpenAI(), agent="zero-shot-react-description")

agent.run("What time is it right now?")
```

The description field is critical — it tells the LLM *when* to use this tool. Vague descriptions lead to agents that ignore your custom logic.

Want to connect a real API? Just swap `get_current_time` for an `requests.get()` call.

**[Try it live →](https://elysiatools.com/en/samples/langchain)**

---

## 5. Multi-Agent Systems — Divide and Conquer

For complex workflows, one agent isn't enough. **Multi-agent systems** distribute tasks across specialized agents.

```python
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.tools import Tool

# Research agent — specializes in finding information
research_agent = initialize_agent(
    tools=[search_tool, wikipedia_tool],
    llm=OpenAI(model="gpt-4"),
    agent="conversational-react-description"
)

# Writing agent — specializes in creating content
writing_agent = initialize_agent(
    tools=[document_tool],
    llm=OpenAI(model="gpt-4"),
    agent="conversational-react-description"
)

# Router — decides who handles each request
def route_request(user_input):
    if any(kw in user_input.lower() for kw in ["research", "find", "look up"]):
        return research_agent
    elif any(kw in user_input.lower() for kw in ["write", "draft", "create"]):
        return writing_agent
    return None

# Usage
task = "Research the history of the internet, then write a summary."
research_results = research_agent.run(task)
final_output = writing_agent.run(f"Summarize this: {research_results}")
```

This mirrors how real teams work — specialists handling their domain, coordinated by a router.

**[Try it live →](https://elysiatools.com/en/samples/langchain)**

---

## 6. RAG with Vector Stores — Give LLMs Your Own Data

The biggest LLM limitation: it doesn't know *your* data. **RAG (Retrieval-Augmented Generation)** fixes this by injecting relevant documents at query time.

```python
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# 1. Load and chunk your documents
loader = TextLoader("company_handbook.txt")
documents = loader.load()

splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)

# 2. Embed and store in vector database
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")

# 3. Create retrieval chain
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

# 4. Query your data
query = "What is our vacation policy?"
result = qa_chain.run(query)
print(result["result"])
```

The LLM answers *only* from your documents. No hallucination about company policies. No training required.

For production scale, swap Chroma for **Pinecone** or **Weaviate** — same API, petabyte-scale vector storage.

**[Try it live →](https://elysiatools.com/en/samples/langchain)**

---

## 7. Structured Output — From Plain Text to JSON

LLMs are great at text, but modern apps need structured data. Use LangChain's output parsers to get clean JSON:

```python
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

# Define your desired schema
response_schemas = [
    ResponseSchema(name="summary", description="A 2-sentence summary of the article"),
    ResponseSchema(name="word_count", description="The approximate word count"),
    ResponseSchema(name="main_topic", description="The main topic or theme"),
    ResponseSchema(name="sentiment", description="The overall sentiment: positive, neutral, or negative")
]

parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = parser.get_format_instructions()

prompt = PromptTemplate(
    input_variables=["article_text"],
    template="Analyze this article:\n{article_text}\n\n{format_instructions}",
    partial_variables={"format_instructions": format_instructions}
)

chain = prompt | OpenAI() | parser

result = chain.invoke({
    "article_text": "Python 3.12 was released with major performance improvements..."
})

# Returns clean Python dict:
# {'summary': '...', 'word_count': 847, 'main_topic': 'Python 3.12 release', 'sentiment': 'positive'}
print(result)
```

This pattern powers every real AI product — summarize emails into tasks, extract contacts from business cards, classify support tickets by priority.

**[Try it live →](https://elysiatools.com/en/samples/langchain)**

---

## The Pattern Behind All of These

Every example above follows the same three-step pattern:

1. **Define** — templates, schemas, tools, memory
2. **Chain** — connect components into a processing pipeline  
3. **Run** — invoke with real data

LangChain's genius is making these composable. A chain can use an agent. An agent uses tools. Tools can use chains. The combinations are infinite, but each piece is simple on its own.

The real unlock comes when you realize: **you don't need to master all of it**. Master chains and memory → you can build chatbots. Add tools → you can build research assistants. Add RAG → you can build enterprise knowledge bases.

Start small. One pattern. Then compose.

---

## What's Still Missing

Here's the problem nobody's solving well yet: **testing LangChain applications**. With traditional code, you write unit tests. With LLM chains, outputs are non-deterministic. How do you regression-test a RAG pipeline when "correct" changes every run?

Some teams use LLM-as-judge (another LLM evaluates outputs), others pin test inputs to specific model snapshots. But the tooling is still young.

If you're building serious LangChain apps, this is the gap worth solving in 2026.

**Explore all LangChain examples → [elysiatools.com/en/samples/langchain](https://elysiatools.com/en/samples/langchain)**
