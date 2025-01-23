import json
import os
from string import Template
from typing import Dict, List

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

from genai_4_dps_helper.watsonx import IBMWatsonx

MY_TEST_TEXTS: List[str] = [
    "The lion is a large carnivorous mammal that lives in the savannas and grasslands of Africa. It is known as the king of the jungle and is a social animal that lives in prides, which are typically made up of several females, their cubs, and one or more males. Lions are skilled hunters and feed on a variety of prey, including zebras, antelopes, and wildebeests. They are also known for their distinctive roars, which can be heard up to five miles away. In the wild, lions can live for up to 12-16 years, although their average lifespan is around 8-10 years due to various threats such as habitat loss, human-wildlife conflict, and poaching. Conservation efforts are underway to protect lion populations and their habitats, including the establishment of national parks and wildlife reserves.",
    "The giant panda is a bear native to China, known for its distinctive black and white markings. It is a herbivore and feeds on bamboo, which makes up 99% of its diet. The giant panda is an endangered species due to habitat loss and low birth rates, with only around 1,800 individuals remaining in the wild. Conservation efforts are underway to protect the giant panda and its habitat, including the establishment of nature reserves and breeding programs. In addition to its distinctive appearance, the giant panda is also known for its unique adaptations, such as its specialized digestive system and its ability to climb trees. Giant pandas are also excellent swimmers and have been known to swim long distances in search of food or shelter.",
    "The blue whale is the largest animal on Earth, with some individuals reaching lengths of up to 100 feet and weighing over 200 tons. It is a filter feeder and feeds on tiny crustaceans and small fish, which it filters through its baleen plates. Blue whales are found in all of the world's oceans and are known for their distinctive songs, which can be heard for hundreds of miles. They are also known for their impressive migration patterns, with some individuals traveling up to 12,000 miles per year. Despite their massive size, blue whales are incredibly streamlined and can reach speeds of up to 30 miles per hour. However, they are threatened by habitat destruction, ship strikes, and entanglement in fishing gear, and conservation efforts are necessary to protect these magnificent creatures.",
    "The cheetah is the fastest land animal on Earth, with the ability to reach speeds of up to 70 miles per hour. It is a carnivore and feeds on small antelopes and other prey, which it catches using its speed and agility. Cheetahs are found in the savannas and grasslands of Africa and are known for their distinctive yellow coats with black spots. They are solitary animals and have large territories, which they mark with their scent. Cheetahs are also diurnal, meaning they are active during the day, and are known for their unique hunting style, which involves stalking their prey and then making a quick sprint to catch it. Unfortunately, cheetahs are threatened by habitat loss and human-wildlife conflict, and conservation efforts are necessary to protect these incredible animals.",
    "The octopus is a highly intelligent and versatile marine animal that is found in oceans around the world. It has eight arms and is known for its ability to change color and camouflage itself, making it a master of disguise. Octopuses are carnivores and feed on a variety of prey, including crustaceans, fish, and other marine animals. They are also known for their unique problem-solving abilities and have been observed using tools to open shells and build shelters. Octopuses have a short lifespan, typically living for around 1-5 years in the wild, although some species can live up to 10 years in captivity. Despite their intelligence and fascinating behavior, octopuses are often misunderstood and are threatened by habitat destruction, overfishing, and climate change.",
    "The giraffe is the tallest mammal on Earth, with some males reaching heights of over 18 feet. It is a herbivore and feeds on leaves, fruits, and flowers from trees and bushes, using its long neck and tongue to reach its food. Giraffes are found in the savannas and grasslands of Africa and are known for their distinctive spots and long necks. They are social animals and live in small groups, called towers, and are known for their unique communication style, which involves using low grunts and moans to communicate with each other. Giraffes are also excellent runners and can reach speeds of up to 35 miles per hour. Unfortunately, giraffes are threatened by habitat loss and human-wildlife conflict, and conservation efforts are necessary to protect these incredible animals.",
    "The kangaroo is a marsupial native to Australia, known for its distinctive hopping ability. It is a herbivore and feeds on grasses, leaves, and other vegetation, using its powerful hind legs to move around. Kangaroos are social animals and live in large groups, called mobs, and are known for their unique social structure, which involves a dominant male leading the group. Kangaroos are also excellent jumpers and can reach heights of up to 6 feet and cover distances of up to 25 feet in a single bound. Unfortunately, kangaroos are threatened by habitat destruction, climate change, and hunting, and conservation efforts are necessary to protect these unique animals.",
    "The penguin is a flightless bird that is found in the Southern Hemisphere, with species ranging from the small little blue penguin to the large emperor penguin. Penguins are carnivores and feed on fish, krill, and other marine animals, which they catch while swimming in the ocean. They are social animals and live in large colonies, often with thousands of individuals, and are known for their unique mating and breeding habits, which involve forming long-term monogamous relationships. Penguins are also excellent swimmers and can reach speeds of up to 25 miles per hour in the water. Unfortunately, penguins are threatened by climate change, habitat destruction, and pollution, and conservation efforts are necessary to protect these charismatic birds.",
    "The tiger is a large carnivorous mammal that is native to Asia, known for its distinctive orange and black stripes. It is a solitary animal and has a large territory, which it marks with its scent. Tigers are skilled hunters and feed on a variety of prey, including deer, wild boar, and other small mammals. They are also known for their unique stripes, which act as camouflage in their natural habitat. Unfortunately, tigers are threatened by habitat loss, poaching, and human-wildlife conflict, and conservation efforts are necessary to protect these majestic animals. Tigers are also apex predators and play a crucial role in maintaining the balance of their ecosystems, making conservation efforts even more important.",
    "The dolphin is a highly intelligent and social marine mammal that is found in oceans around the world. It is a carnivore and feeds on fish, squid, and other marine animals, which it catches using its echolocation abilities. Dolphins are known for their playful behavior and ability to communicate with each other using clicks and whistles. They are also highly social animals and live in large groups, called pods, and are known for their unique social structure, which involves cooperation and altruism. Dolphins are also known for their intelligence and have been observed using tools and solving complex problems. Unfortunately, dolphins are threatened by habitat destruction, overfishing, and pollution, and conservation efforts are necessary to protect these incredible animals.",
]


MODEL_NAME = "meta-llama/llama-3-3-70b-instruct"

parameters: Dict = {
    GenParams.DECODING_METHOD: DecodingMethods.SAMPLE.value,
    GenParams.MIN_NEW_TOKENS: 0,
    GenParams.MAX_NEW_TOKENS: 250,
    GenParams.TEMPERATURE: 0.7,
    GenParams.TOP_P: 1,
    GenParams.TOP_K: 50,
    GenParams.RANDOM_SEED: 2973559815,
    GenParams.REPETITION_PENALTY: 1,
}


watsonx: IBMWatsonx = IBMWatsonx(
    model_name=MODEL_NAME,
    watsonx_params=parameters,
    project_id=os.getenv("WML_WATSONX_AI_PROJECT_ID"),
    credentials=Credentials(
        api_key=os.getenv("WML_WATSONX_AI_API_KEY"),
        url=os.getenv("WML_WATSONX_AI_ENDPOINT"),
    ),
)

print("Chat Models")
watsonx.list_chat_models()
print("Embedding Models")
watsonx.list_embedding_models()

prompt_template = Template("""<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
You are a helpful assistant whose job is to keep everyone happy and content by always ending your responses with a Dad Joke<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Examine the text within the backticks ``` and provide a concise summary, use bullet points and at most the two most important items.
```
$text                           
```

Your summary is
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
""")

prompts: List[str] = [
    prompt_template.substitute(text=test_text) for test_text in MY_TEST_TEXTS
]
summaries_with_jokes = watsonx.send_to_watsonxai(prompts=prompts)

print(json.dumps(summaries_with_jokes, indent=2))
