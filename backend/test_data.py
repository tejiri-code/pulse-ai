"""
Test data for offline demo
Provides 5 realistic AI/ML news articles for demonstration
"""

DEMO_NEWS_ITEMS = [
    {
        "title": "GPT-4.5 Turbo: OpenAI's Latest Model Achieves 95% on MMLU Benchmark",
        "url": "https://openai.com/research/gpt-4.5-turbo",
        "source": "blog",
        "content": """OpenAI has released GPT-4.5 Turbo, the latest iteration of their flagship language model. The new model achieves 95% accuracy on the MMLU (Massive Multitask Language Understanding) benchmark, a significant improvement over GPT-4's 86.4%. Key improvements include enhanced reasoning capabilities, better context retention up to 128K tokens, and a 40% reduction in hallucinations. The model also demonstrates stronger performance on coding tasks, achieving 92% on HumanEval compared to GPT-4's 67%. OpenAI credits the improvements to a novel training technique called "Constitutional Reinforcement Learning" that better aligns the model with human values and factual accuracy. The model will be available via API starting next week with pricing 20% lower than GPT-4.""",
        "published_date": "2024-12-02T08:00:00Z"
    },
    {
        "title": "DeepMind's AlphaFold 3 Predicts Protein-Ligand Interactions with 90% Accuracy",
        "url": "https://arxiv.org/abs/2024.12345",
        "source": "arxiv",
        "content": """Researchers at DeepMind have unveiled AlphaFold 3, a breakthrough in computational biology that can predict how proteins interact with small molecules (ligands) with 90% accuracy. This represents a major leap forward in drug discovery, potentially reducing the time to identify promising drug candidates from years to weeks. The model builds on AlphaFold 2's protein structure prediction by incorporating quantum mechanical principles and molecular dynamics simulations. In blind tests against experimental data, AlphaFold 3 correctly predicted binding sites and binding affinities for 1,200 out of 1,350 protein-ligand pairs. The implications for pharmaceutical research are enormous, with early trials showing successful identification of novel inhibitors for cancer targets. The model uses a transformer-based architecture with 560M parameters and was trained on over 1 billion protein-ligand interactions from the Protein Data Bank.""",
        "published_date": "2024-12-01T14:30:00Z"
    },
    {
        "title": "Meta's LLaMA 3.1: 70B Open-Source Model Rivals GPT-4 on Most Benchmarks",
        "url": "https://github.com/meta-llama/llama3.1",
        "source": "github",
        "content": """Meta AI has open-sourced LLaMA 3.1, a 70-billion parameter language model that matches or exceeds GPT-4's performance on most standard benchmarks while remaining fully open-source. The model achieves 84.2% on MMLU, 89.5% on GSM8K math problems, and 78.3% on the challenging MATH benchmark. Unlike previous LLaMA versions, 3.1 was trained with a focus on instruction following and has undergone extensive safety tuning. The training dataset includes 2.5 trillion tokens, with a carefully curated mix of web text, code, mathematical reasoning, and multilingual content. Meta has also released fine-tuned variants specialized for coding (LLaMA-Code) and creative writing (LLaMA-Creative). The models are released under a permissive license allowing commercial use. Early adopters report that the 70B model runs efficiently on a single A100 GPU with quantization, making it accessible to researchers and small companies.""",
        "published_date": "2024-12-01T16:00:00Z"
    },
    {
        "title": "Anthropic's Constitutional AI: A New Paradigm for Safe Language Models",
        "url": "https://www.anthropic.com/research/constitutional-ai-v2",
        "source": "blog",
        "content": """Anthropic has published a comprehensive paper on Constitutional AI (CAI), a novel training methodology that embeds safety and ethical guidelines directly into language models during training. Unlike traditional RLHF (Reinforcement Learning from Human Feedback), CAI uses a written "constitution" of principles that the model learns to follow autonomously. The researchers demonstrate that CAI models refuse harmful requests 99.2% of the time compared to 73.4% for standard RLHF models, while maintaining helpfulness on benign queries. The constitution includes principles like "Choose the response that is most helpful, harmless, and honest" and "Prefer responses that avoid bias and stereotyping." Significantly, the CAI approach reduces the need for human labelers, as models can self-critique and self-improve based on constitutional principles. Anthropic has open-sourced their constitution and training code, encouraging the AI community to experiment with different value frameworks.""",
        "published_date": "2024-11-30T10:00:00Z"
    },
    {
        "title": "Google Brain's Gemini Ultra: Multimodal AI Outperforms Humans on Complex Tasks",
        "url": "https://blog.google/technology/ai/gemini-ultra-multimodal-breakthrough",
        "source": "blog",
        "content": """Google has announced Gemini Ultra, a multimodal AI model that can process and reason across text, images, audio, and video simultaneously. In a landmark achievement, Gemini Ultra scored 92.4% on the MMMU (Massive Multi-discipline Multimodal Understanding) benchmark, surpassing human expert performance of 88.6%. The model demonstrates unprecedented cross-modal reasoning, such as solving physics problems by analyzing diagrams, debugging code by examining screenshots, and answering medical questions using patient X-rays. Gemini Ultra uses a unified transformer architecture with 1.8 trillion parameters and was trained on a diverse dataset including 3 trillion text tokens, 800 million images, and 20 million hours of video. Key innovations include a novel attention mechanism that dynamically adjusts to input modality and a training technique called "Modality-Aware Pretraining." Google plans to integrate Gemini Ultra into Search, Workspace, and Cloud AI products throughout 2024. Initial access will be available via API for enterprise customers, with consumer applications to follow.""",
        "published_date": "2024-11-29T12:00:00Z"
    }
]


# Expected summaries (for reference)
DEMO_SUMMARIES = [
    {
        "news_item_id": 1,
        "three_sentence_summary": "OpenAI has released GPT-4.5 Turbo, achieving 95% on the MMLU benchmark and representing a major leap in language model capabilities. The model features enhanced reasoning, 128K token context, 40% fewer hallucinations, and 92% accuracy on coding tasks. These improvements stem from a new Constitutional Reinforcement Learning technique that better aligns the model with human values and factual accuracy.",
        "social_hook": "🚀 GPT-4.5 Turbo just dropped! 95% MMLU, 92% HumanEval, 40% fewer hallucinations, and 20% cheaper. Constitutional RL is a game-changer for AI alignment. #AI #OpenAI #GPT4",
        "tags": ["OpenAI", "GPT-4", "LLM", "Benchmarks", "AI Alignment"]
    },
    {
        "news_item_id": 2,
        "three_sentence_summary": "DeepMind's AlphaFold 3 revolutionizes drug discovery by predicting protein-ligand interactions with 90% accuracy. The model combines AlphaFold 2's protein structure prediction with quantum mechanics and molecular dynamics, correctly predicting 1,200 out of 1,350 binding pairs in blind tests. This breakthrough could reduce drug candidate identification from years to weeks, with major implications for pharmaceutical research.",
        "social_hook": "💊 AlphaFold 3 achieves 90% accuracy in protein-ligand prediction! Drug discovery just got 10x faster. The quantum mechanics integration is brilliant. #DeepMind #AlphaFold #DrugDiscovery #AI",
        "tags": ["DeepMind", "AlphaFold", "Biology", "Drug Discovery", "Protein Folding"]
    },
    {
        "news_item_id": 3,
        "three_sentence_summary": "Meta has open-sourced LLaMA 3.1 70B, matching GPT-4 performance on most benchmarks while remaining fully accessible to researchers and companies. The model achieves 84.2% on MMLU and includes specialized variants for coding and creative writing, trained on 2.5 trillion tokens. With efficient inference on a single A100 GPU, LLaMA 3.1 democratizes access to state-of-the-art language models.",
        "social_hook": "🦙 LLaMA 3.1 is HERE! 70B params, GPT-4-level performance, 100% open-source, commercial-friendly, runs on 1x A100. The AI landscape just changed. #Meta #LLaMA #OpenSource #AI",
        "tags": ["Meta", "LLaMA", "Open Source", "LLM", "Benchmarks"]
    },
    {
        "news_item_id": 4,
        "three_sentence_summary": "Anthropic introduces Constitutional AI v2, embedding safety principles directly into model training to achieve 99.2% harmful request refusal rates. Unlike traditional RLHF, CAI uses a written constitution of ethical guidelines, enabling models to self-critique and improve autonomously. The open-sourcing of both the constitution and training code encourages community experimentation with different value frameworks.",
        "social_hook": "🛡️ Constitutional AI v2: 99.2% harmful refusal rate, self-improving models, open-source framework. The future of AI alignment looks promising! #Anthropic #AISafety #Ethics #AI",
        "tags": ["Anthropic", "AI Safety", "Constitutional AI", "Ethics", "RLHF"]
    },
    {
        "news_item_id": 5,
        "three_sentence_summary": "Google's Gemini Ultra achieves 92.4% on the MMMU benchmark, surpassing human expert performance at 88.6% through unified multimodal reasoning. The 1.8 trillion parameter model processes text, images, audio, and video using a novel Modality-Aware Pretraining technique. Integration into Google's product ecosystem throughout 2024 will bring multimodal AI to billions of users.",
        "social_hook": "🌟 Gemini Ultra BEATS human experts! 92.4% on MMMU, 1.8T params, true multimodal AI. Cross-modal reasoning is finally here. The future is now. #Google #Gemini #Multimodal #AI",
        "tags": ["Google", "Gemini", "Multimodal", "Benchmarks", "Computer Vision"]
    }
]


if __name__ == "__main__":
    import json
    print("Demo Test Data:")
    print(json.dumps(DEMO_NEWS_ITEMS, indent=2))
