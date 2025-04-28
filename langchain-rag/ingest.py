from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from typing import List, Dict

def convert_metadata(metadata: Dict) -> Dict:
    converted = {}
    for key, value in metadata.items():
        if isinstance(value, list):
            converted[key] = ", ".join(str(v) for v in value)
        else:
            converted[key] = value
    return converted

# All characters from the Italian Brainrot universe
raw_documents = [
    # Original characters
    Document(
        page_content="Tralalero Tralala: A shark wearing Nike shoes, known for playing Fortnite. The original and most iconic Italian Brainrot character that started the entire trend. Often seen dancing and making exaggerated movements while playing Fortnite, particularly known for its floss dance. The character represents the fusion of modern gaming culture with absurdist humor.",
        metadata={
            "name": "Tralalero Tralala",
            "category": "aquatic",
            "features": ["shark", "Nike shoes", "blue sneakers", "Fortnite dance moves", "gaming headset", "exaggerated expressions"],
            "origin": "Early January 2025 by TikTok user @eZburger401",
            "catchphrase": "Tralalero Tralala, porco dio e porco Allah",
            "related_characters": ["Squalo Gaming", "Pesciolino Stream"]
        }
    ),
    Document(
        page_content="Bombardiro Crocodilo: An anthropomorphic crocodile military bomber plane hybrid. Known for its military aesthetic and dramatic presence. The character embodies the absurdist combination of military hardware with animal features, often seen performing elaborate aerial maneuvers while maintaining its serious demeanor. Popular in military-themed Italian Brainrot memes.",
        metadata={
            "name": "Bombardiro Crocodilo",
            "category": "military",
            "features": ["crocodile head", "bomber plane body", "military aesthetic", "camouflage patterns", "working propellers", "military medals", "aviator goggles"],
            "origin": "Mid-February 2025 on TikTok",
            "related_characters": ["Generale Serpente", "Capitano Caimano"]
        }
    ),
    Document(
        page_content="Chimpanzini Bananini: A hybrid creature that's half banana and half monkey, known for its goofy and confused expression. The character has become a symbol of the meme's absurdist humor, often seen in situations where it questions its own existence. Its banana body peels slightly when stressed, revealing more monkey features underneath.",
        metadata={
            "name": "Chimpanzini Bananini",
            "category": "food-animal-hybrid",
            "features": ["banana body", "monkey features", "confused expression", "peelable skin", "monkey tail", "banana-shaped hands"],
            "related_characters": ["Orangini Meloni", "Gorillini Frutti"]
        }
    ),
    Document(
        page_content="Lirili Larila: A cactus elephant hybrid walking in the desert with flippers, wearing sandals. This surreal character combines desert survival with impractical beach gear, creating a perfect embodiment of Italian Brainrot's love for contradictory elements. Known for its gentle demeanor despite its prickly exterior.",
        metadata={
            "name": "Lirili Larila",
            "category": "plant-animal-hybrid",
            "features": ["cactus body", "elephant features", "sandals", "flippers", "desert-adapted skin", "water-storing trunk", "flowering spines"],
            "origin": "March 2025 by @desertmemer",
            "related_characters": ["Succulento Elephanto", "Deserti Bestia"]
        }
    ),
    Document(
        page_content="Brr Brr Patapim: A hybrid between a forest and a monkey with large feet. Popular on TikTok and YouTube for its distinctive walking sound effects and the way it combines an entire ecosystem with primate features. The character's body contains a miniature functioning forest ecosystem, complete with small animals and weather patterns.",
        metadata={
            "name": "Brr Brr Patapim",
            "category": "nature-animal-hybrid",
            "features": ["forest elements", "monkey features", "large feet", "internal ecosystem", "weather effects", "glowing fireflies", "rustling leaves"],
            "origin": "Late March 2025",
            "related_characters": ["Foresta Scimmia", "Jungle Jumper"]
        }
    ),
    Document(
        page_content="Cappuccino Assassino: An early character that was initially forgotten but gained new life through related characters. This mysterious coffee-based assassin moves silently through the Italian Brainrot universe, leaving only the aroma of perfectly brewed espresso in its wake. Known for its stealth abilities and the steam that rises from its head when agitated.",
        metadata={
            "name": "Cappuccino Assassino",
            "category": "beverage",
            "features": ["coffee elements", "mysterious appearance", "steam effects", "barista weapons", "coffee bean armor", "espresso-shot capabilities"],
            "related_characters": ["Ballerina Cappuccina", "Ballerino Lorololo", "Espressona Signora"]
        }
    ),
    Document(
        page_content="Ballerina Cappuccina: A ballet-dancing coffee cup character, wife of Cappuccino Assassino. She performs elegant pirouettes while maintaining perfect coffee temperature and crema. Her movements create beautiful patterns of steam in the air, and she's known for her signature move 'The Grande Caffè Twist'.",
        metadata={
            "name": "Ballerina Cappuccina",
            "category": "beverage",
            "features": ["ballet outfit", "coffee cup body", "graceful movements", "perfect crema", "steam ribbons", "porcelain tutu", "coffee aroma trail"],
            "related_characters": ["Cappuccino Assassino", "Ballerino Lorololo"]
        }
    ),
    Document(
        page_content="Frigo Camelo: A camel merged with a refrigerator, representing the absurdity of the Italian Brainrot universe. This character maintains perfect temperature control in desert environments, storing cold drinks in its humps. Famous for its ability to dispense ice cubes from its nose and keep food fresh for weeks in harsh conditions.",
        metadata={
            "name": "Frigo Camelo",
            "category": "appliance-animal-hybrid",
            "features": ["camel head", "refrigerator body", "temperature controls", "ice dispenser", "storage compartments", "cooling humps", "energy-efficient design"],
            "related_characters": ["Freezer Fennec", "Cool Camelus"]
        }
    ),
    Document(
        page_content="Boneca Ambalabu: An Indonesian Brainrot character that is a hybrid between a frog and a tire with human legs. This character represents the international spread of the meme, combining Indonesian automotive culture with amphibian features. Known for its unique bouncing movement and ability to inflate itself for improved suspension.",
        metadata={
            "name": "Boneca Ambalabu",
            "category": "indonesian-variant",
            "features": ["frog head", "tire body", "human legs", "tread patterns", "inflatable body", "jumping ability", "rubber skin"],
            "origin": "February 2nd, 2025 by @ofuscabreno"
        }
    ),
    Document(
        page_content="Tung Tung Tung Sahur: An Indonesian spin-off character known for appearing during Sahur (pre-dawn meal during Ramadan). This character combines traditional Indonesian Ramadan wake-up calls with the surreal elements of Italian Brainrot. It produces musical sounds by drumming on its own body and helps wake people for their pre-dawn meals.",
        metadata={
            "name": "Tung Tung Tung Sahur",
            "category": "indonesian-variant",
            "features": ["mysterious appearance", "rhythmic sound", "religious connection", "glowing body parts", "musical instruments", "traditional clothing", "dawn-sensing abilities"],
            "related_characters": ["Bedug Warrior", "Ramadan Runner"]
        }
    ),
    # Add metadata about the trend itself
    Document(
        page_content="Italian Brainrot refers to a series of AI-generated characters that combine animals with objects or give them anthropomorphic features. The videos typically feature Italian text-to-speech voices rhyming the characters' names with absurd statements. The phenomenon has evolved into a global meme movement, with particularly strong followings in Italy and Indonesia, spawning countless fan creations and character variations while maintaining its signature absurdist style.",
        metadata={
            "category": "metadata",
            "name": "metadata",
            "features": ["AI-generated imagery", "Italian/Indonesian text-to-speech", "Absurd character combinations", "Viral social media presence", "Community-driven world building", "Cross-cultural adaptations", "Rhyming name patterns", "Surreal character interactions"],
            "trend_start": "January 2025",
            "primary_platform": "TikTok"
        }
    )
]

# Convert metadata for all documents
documents = [
    Document(
        page_content=doc.page_content,
        metadata=convert_metadata(doc.metadata)
    )
    for doc in raw_documents
]

def ingest_documents():
    # Initialize embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Initialize ChromaDB
    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )
    
    # Add documents to ChromaDB
    vectorstore.add_documents(documents)
    print(f"Added {len(documents)} documents to ChromaDB")

if __name__ == "__main__":
    ingest_documents() 