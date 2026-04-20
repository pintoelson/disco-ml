# Discussion #8722: Multi-agent CXR analysis system
**Repository:** Project-MONAI/MONAI
**Author:** shauryaq05
**Created At:** 2026-01-29T14:00:36Z

## Description
ello community,

I'm building a multi-agent chest X-ray analysis system for my academic project with a tight 2-day deadline. The system consists of:
Base Model: CXR-LLAVA from Hugging Face for initial image analysis

Three Specialized Agents (using CrewAI):

Device Detection Agent
Serious Flagging Agent
Confidence Assignment Agent
Orchestrator: Coordinates all agents

Current Issues:
CXR-LLAVA Integration: Getting dependency conflicts (PyTorch/Transformers version issues) when loading the model Agent Orchestration: Agents aren't properly passing results to each other in the pipeline
Error Handling: When one agent fails, the whole system crashes  
Here is the GitHub link for your reference : https://github.com/[shauryaq05/CXR-Analysis](https://github.com/shauryaq05/CXR-Analysis)
