# Optical Character Recognition of food ingredients

### Idea
Main purpose of this project is to create an easy-to-use application that will be able to assess the harmfulness of any food product. 

This will be done in several steps:
1. The user takes a photo of a list of ingredients,
2. The image is processed and forwarded to OCR,
3. Each recognized word is compared to all database records to determine the most likely result,
4. If the user decides to leave all recognized words, a page is displayed listing all the ingredients and the overall harmfulness of the product. The user can check each substance - for its description and classification,
5. If the user wants to edit a word, they firstly receive the 3 most likely results. If none of them are correct, the user can send a request to add the ingredient to the database,
6. If the word has a very low resemblance to each database record, the user is informed, that the word is not recognized and decides to reject it or send a request to add the ingredient to the database.

### Project Layout
* Image to text - this part is responsible for image pre-processing and applying OCR on the photo
* Database management - creates a database of food ingredients with their description, category, and harmfulness grade. It also allows basic communication with the database.
* Text comparison - prepares recognized text (removes spaces and invalid characters). Then it connects to the database and browses each record, looking for the most similar words. To compare recognized text and records, it uses the fuzzywuzzy library (Levenshtein Distance implementation).
### Task Status

### Important Note
