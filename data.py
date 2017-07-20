import json

import numpy as np

from config import RELATIONSHIPS, OBJECTS


class VisualGenomeRelationshipsDataset():
    def __init__(self, object_to_idx={}, relationships_to_idx={}, data_path="data/relationships.json"):
        self.data = json.load(open(data_path, "r"))
        self.relationships_to_idx = relationships_to_idx
        self.objects_to_idx = object_to_idx
        self.objects_counter = 0
        self.relationships_counter = 0
        self.nb_images = len(self.data)
        self.nb_relationships = 0
        self.image_ids = []
        self.relationships = []
        self.objects_regions = []  # h, w, x, y
        self.subjects_regions = []  # h, w, x, y

    def get_regions(self, object):
        return object["h"], object["w"], object["x"], object["y"]

    def get_object_idx(self, object_name):
        if object_name in self.objects_to_idx.keys():
            return self.objects_to_idx[object_name]
        else:
            self.objects_counter += 1
            self.objects_to_idx[object_name] = self.objects_counter
            return self.objects_to_idx[object_name]

    def get_relationship_idx(self, predicate):
        if predicate in self.relationships_to_idx.keys():
            return self.relationships_to_idx[predicate]
        else:
            self.relationships_counter += 1
            self.relationships_to_idx[predicate] = self.relationships_counter
            return self.relationships_to_idx[predicate]

    def get_object_name(self, rel_data, object_type):
        if "name" in rel_data[object_type].keys():
            return rel_data[object_type]["name"]
        else:
            return rel_data[object_type]["names"][0]

    def build_dataset(self):
        for i in range(self.nb_images):
            image_id = self.data[i]["image_id"]
            relationships = self.data[i]["relationships"]
            for j, rel_data in enumerate(relationships):
                object_name = self.get_object_name(rel_data, "object")
                object_id = self.get_object_idx(object_name)
                subject_name = self.get_object_name(rel_data, "subject")
                subject_id = self.get_object_idx(subject_name)
                relationship_id = self.get_relationship_idx(rel_data["predicate"])
                self.relationships += [(object_id, relationship_id, subject_id)]
                self.objects_regions += [self.get_regions(rel_data["object"])]
                self.subjects_regions += [self.get_regions(rel_data["subject"])]
                self.image_ids += [image_id]
        self.nb_relationships = i + j
        self.objects_regions = np.array(self.objects_regions)
        self.subjects_regions = np.array(self.subjects_regions)
        self.image_ids = np.array(self.image_ids)
        self.relationships = np.array(self.relationships)
        return self.image_ids, self.relationships, self.objects_regions, self.subjects_regions
