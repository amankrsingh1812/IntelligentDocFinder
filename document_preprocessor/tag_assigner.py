import pickle
from utils import calculate_cosine_similarity


def assign_tags(doc_paragraphs_embeddings: list, csim_threshold=0.8) -> list:
    tags_map = pickle.load(open("document_preprocessor/tags.pickle", "rb"))
    
    tags_set = set()
    most_similar_tag_score = -1
    most_similar_tag = ""
    
    for para_embed in doc_paragraphs_embeddings:
        paragraph_tags_set, para_most_similar_tag, para_most_similar_tag_score = assign_tags_for_paragraph(para_embed, tags_map, csim_threshold)
        if len(paragraph_tags_set) > 0:
            tags_set.union(paragraph_tags_set)
        elif para_most_similar_tag_score >= most_similar_tag_score:
            most_similar_tag = para_most_similar_tag
            most_similar_tag_score = para_most_similar_tag_score
            print("[Testing]: Tag score =", most_similar_tag_score)
    
    tags_list = list(tags_set)

    if len(tags_list) == 0 and most_similar_tag_score > -1:
        tags_list = [most_similar_tag]
    
    return tags_list


def assign_tags_for_paragraph(paragraphs_embeddings: list, tags_map: map, csim_threshold: float) -> set:
    paragraph_tags_set = set()
    most_similar_tag = ""
    most_similar_tag_score = -1
    
    for tag, tag_embeddings in tags_map.items():
        curr_similarity_score = calculate_cosine_similarity(paragraphs_embeddings, tag_embeddings)
        
        if curr_similarity_score >= csim_threshold:
            paragraph_tags_set.add(tag)
        
        if curr_similarity_score >= most_similar_tag_score:
            most_similar_tag_score = curr_similarity_score
            most_similar_tag = tag
        
    return paragraph_tags_set, most_similar_tag, most_similar_tag_score