import autogen

# Replace "" with your actual OpenAI API Key
OPENAI_API_KEY = ""

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-3.5-turbo"],
    },
)

llm_config = {"config_list": config_list, "cache_seed": 42, "api_key": OPENAI_API_KEY}
prompt="Find a latest paper about gpt-4 on arxiv and find its potential applications in software."

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={
        "last_n_messages": 2,
        "work_dir": "groupchat",
        "use_docker": False,  # You can set this to True if Docker is available (safer for code execution)
    },
    human_input_mode="TERMINATE",
)
print("hello")
coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config.copy(),  # Create a copy to avoid reference issues
)

pm = autogen.AssistantAgent(
    name="Product_manager",
    system_message="Creative in software product ideas.",
    llm_config=llm_config.copy(),  # Create a copy to avoid reference issues
)

groupchat = autogen.GroupChat(agents=[user_proxy, coder, pm], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config.copy())
default_model = "gpt-4"  # Default model to use if the config_list is empty

if llm_config["config_list"]:  # Check if the list is not empty
    model = llm_config["config_list"][0].get("model", default_model)
    user_proxy.initiate_chat(
        manager, messages="add two number in python", model=model
    )
else:
    print("Error: No models found in config_list")

print("hey")



