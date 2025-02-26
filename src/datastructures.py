
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        # example list of members
        self._members = [
            {
                "id": self._next_id,
                "first_name": "John",
                "last_name": "Jackson",
                "age": 33,
                "lucky_numbers": [7, 13, 22]
            },
             {
                "id": self._next_id +1,
                "first_name": "Jane",
                "last_name": "Jackson",
                "age": 35,
                "lucky_numbers": [10, 14, 3]
            },
             {
                "id": self._next_id +2,
                "first_name": "Jimmy",
                "last_name": "Jackson",
                "age": 5,
                "lucky_numbers": [1]
            }
        ]

    
    def _generateId(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        
        new_member = {
        "id": self._generateId(),
        "first_name": member["first_name"],
        "last_name": self.last_name,  
        "age": member["age"],
        "lucky_numbers": member["lucky_numbers"],
        }
        self._members.append(new_member)
        return new_member  


    def delete_member(self, id):
        for member in self._members:
            if member["id"] == id:
                self._members.remove(member)
                return True  
        return False 

    def update_member(self, id, new_data):
        for member in self._members:
            if member["id"] == id:
                member.update(new_data)
                return member


    def get_member(self, id):
        for member in self._members:
            if member["id"] == id:
                return member

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members
