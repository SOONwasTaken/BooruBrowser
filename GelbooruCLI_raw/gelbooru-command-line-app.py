import requests
import os

# Grabs images from Gelbooru using the API.

urlEncode = {
    "!":  "%21",
    "\"": "%22",
    "#":  "%23",
    "$":  "%24",
    "%":  "%25",
    "&":  "%26",
    "'":  "%27",
    "(":  "%28",
    ")":  "%29",
    "*":  "%2a",
    "+":  "%2b",
    ",":  "%2c",
    "-":  "%2d",
    ".":  "%2e",
    "/":  "%2f",
    ":":  "%3a",
    ";":  "%3b",
    "<":  "%3c",
    "=":  "%3d",
    ">":  "%3e",
    "?":  "%3f",
    "@":  "%40",
    "[":  "%5b",
    "\\": "%5c",
    "]":  "%5d",
    "^":  "%5e",
    "_":  "%5f",
    "`":  "%60",
    "{":  "%7b",
    "|":  "%7c",
    "}":  "%7d",
    "~":  "%7e"
}

urlEncodeKeys = list(urlEncode.keys())

acceptableAnswersY = ['y', 'yes', '1']
acceptableAnswersN = ['n', 'no', '0']

"""
getPosts()

Method for getting images via the Post API.

From Gelbooru:
Url for API access: /index.php?page=dapi&s=post&q=index

Params:
    - limit: How many posts you want to retrieve.      
             There is a default limit of 100 posts 
             per request.
    
    - pid: The page number.
    
    - tags: The tags to search for. Any tag combination that 
            works on the web site will work here.
    
    - cid: Change ID of the post. This is in Unix time so 
           there are likely others with the same value if 
           updated at the same time.
    
    - id: The post id.
    
    - json: Set to 1 for JSON formatted response.

Experiment if pid can be used to page into the response by
limit. ex: limit = 10 is page size of 10 for each pid.
"""
def getPosts(limit: int = 100, tags: list[str] = [], pid = 0, ratings: list[str] = ['general'], suppressPrint: bool = False) -> list:
    
    batches = {}
    for rating in ratings:
        """
        Gelbooru will sometimes require authentication for the API.
        Get the parameters for the API key and User ID to add to the
        link.

        Include a txt file named apiKey.txt in the same directory
        as the executable with the following line:

        &api_key=API_KEY_HERE&user_id=USER_ID_HERE

        Requires a Gelbooru account. This info can be found in the
        account options or profile pages.
        """
        apiKey = ''
        with open('apiKey.txt', 'r') as file:
            apiKey = file.readlines()[0]

        url = 'https://gelbooru.com/index.php?page=dapi&s=post&q=index' + apiKey + \
              '&limit=' + str(limit)
    
        # Properly encode characters for HTTP
        tagsEncoded = []
        for tag in tags:
            temp = ''
            for char in tag: 
                temp += urlEncode[char] if char in urlEncodeKeys else char    
            tagsEncoded.append(temp)
        url += '&tags=' + '+'.join(tagsEncoded)
    
        # Ratings have their own meta tag to filter by.
        url += '+rating' + urlEncode[":"] + rating
        
        # pid is the page number
        url += '&pid=' + str(pid)

        # Format response as JSON
        url += '&json=1'

        response = requests.get(url, stream = True).json()
    
        if not suppressPrint: print(f"\nGetting image(s) for {rating}...")

        """
        Gelbooru response contains two keys:

        @attributes: 
            A dictionary containing information
            about the request.

            ex: {'limit': 10, 'offset': 0, 'count': 2043}

        post:
            A dictionary containing posts of length equal
            to that of 'limit'.

        Please refer to api-info.txt for all fields contained
        within a post.
        """
        batches[rating] = response

    return batches

    """
    TODO: 
    - Request the image from the link in the response.
    - Write the image to the img/ folder.
    - Use user input to make more friendly
    - Paging (use pid argument)
    - Get full or sample sized images
    """

def askUserForRatingPreferences(rating: str) -> bool:
    yesOrNo = ''
    while yesOrNo == '':
        temp = input(f"\nInclude {rating} posts in search? (y / n, yes / no, 1 / 0)\n>>> ").lower().strip()
        
        if temp not in acceptableAnswersY and temp not in acceptableAnswersN:
            print("Please enter a valid answer.\n")
            continue
        
        yesOrNo = temp
    
    return yesOrNo in acceptableAnswersY

def main():

    # Create paths if they do not exist
    absolutePath = os.path.dirname(os.path.abspath(__file__))
    imgFolder = os.path.join(absolutePath, 'img')
    generalPath = os.path.join(imgFolder, 'general')
    sensitivePath = os.path.join(imgFolder, 'sensitive')
    questionablePath = os.path.join(imgFolder, 'questionable')
    explicitPath = os.path.join(imgFolder, 'explicit')
    mode = 0o666

    if not os.path.isdir(imgFolder): os.mkdir(imgFolder, mode)
    if not os.path.isdir(generalPath): os.mkdir(generalPath, mode)
    if not os.path.isdir(sensitivePath): os.mkdir(sensitivePath, mode)
    if not os.path.isdir(questionablePath): os.mkdir(questionablePath, mode)
    if not os.path.isdir(explicitPath): os.mkdir(explicitPath, mode)

    print(\
    """                                            
                                    ░░▓           
       ░▓▓▓▓▓▓▓░░              ░▓▓▓▓▓▓▓           
       ░▓   ░▓▓▓▓▓▓▓▓▓░       ▒▓▓▓▓▓▓▓▓           
        ▓     ░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓           
        ░▓   ░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         
         ▓░  ░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         
         ░▓░ ░▓▓▓▓▓▓▓▓▓▓▒░       ░▒▓▓▓▓▓▓         
          ░▓▓▓▓▓▓▓▓▓▓▓░              ░▓▓▓         
            ▓▓▓▓▓▓▓▓▓                             
           ▓▓▓▓▓▓▓▓▓                              
           ▓▓▓▓▓▓▓▓▓                              
           ▓▓▓▓▓▓▓▓▒      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         
           ▓▓▓▓▓▓▓▓▒      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         
           ▓▓▓▓▓▓▓▓▓      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         
           ░▓▓▓▓▓▓▓▓▒           ░▓▓▓▓▓▓▓▓         
            ▓▓▓▓▓▓▓▓▓▓          ░▓▓▓▓▓▓▓▓         
             ▓▓▓▓▓▓▓▓▓▓▓        ░▓▓▓▓▓▓▓▓         
              ▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         
              ░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         
            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░     
          ░▓▓▓▓▓▓▓▓▓▓▓▓▓▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
          ▓▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░ 
          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░
          ▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░      ░▓▓▓▓▓▓▓▓
           ░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░                ░▓▓▓▓ 
               ▒▓▓▓░  

    ==== Welcome to Gelbooru Command Line Tool. ====
    """)
    
    while True:
        
        answer = input("\nPress Enter to start, or type 'q' to quit.\n>>> ").strip().lower()
        if answer == 'q': break

        limit = 0
        while limit == 0:
            limInput = input("\nHow many images per rating batch (1 to 100)?\n>>> ").strip()

            if not limInput.isdigit() and not limInput.lstrip('-').isdigit():
                print(f"Batch amount must be a numerical input.\n")
                continue
        
            limitAsInt = int(limInput)
            if limitAsInt <= 0 or limitAsInt > 100 :
                print("Batch amount must be a number in the range of 1 to 100 (inclusive).\n")
                continue

            limit = limitAsInt

        tags = []
        while tags == []:
            tagInput = \
            input(\
            "\nPlease enter tags to search for. Use a space separated list.\n" + 
            "e.g.: 1girl solo blush glasses looking_at_viewer\n>>> ")

            normalized = tagInput.lower().strip()

            if not normalized:
                print("You must enter at least one tag.\n")
                continue
        
            tags = normalized.split()
    
        tags = [tag.lower() for tag in tags]

        print(\
        """
Select ratings that can be included in your search. Criteria for ratings is given
by Gelbooru as follows:

    - General: 
        G-rated content. Content that is completely safe for work. Nothing 
        sexualized or inappropriate to view in front of others.

    — Sensitive:
        Ecchi, sexy, suggestive, or mildly erotic content. Skimpy or 
        revealing_clothes, swimsuits, underwear, images focused on the breasts 
        or ass, and any other content that is potentially not safe for work.

    — Questionable:
        Softcore erotica. Simple nudity or near-nudity, but no explicit sex or 
        exposed genitals.

    — Explicit:
        Blatantly sexual content. Explicit sex acts, exposed genitals, and sexual 
        fluids.

    A more detailed explanation can be found at 
    https://gelbooru.com/index.php?page=wiki&s=view&id=2535

Note: Due to a limitation with how Gelbooru filters meta tags (including ratings),
you are unable to filter by multiple at a time. You will receive images up to a
maximum of your selected batch amount for each rating.
        """)

        ratings = ['General', 'Sensitive', 'Questionable', 'Explicit']
        selectedRatings = []
        while selectedRatings == []:
        
            ratingInput = []

            for rating in ratings:
                if askUserForRatingPreferences(rating):
                    ratingInput.append(rating.lower())

            if not ratingInput:
                print("You must choose at least one option.\n")
                continue

            selectedRatings = ratingInput

        print("\nPage count(s):")
        tempBatch = getPosts(1, tags, 0, selectedRatings, True)
        for rating in selectedRatings:
            count = tempBatch[rating]['@attributes']['count']
            print(f"rating:{rating} - {count if count // limit == count else count // limit + 1}")
        
        pid = ''
        while not pid.isdigit():
            answer = input(f"\nPlease enter a page number to go to start at.\n>>> ")

            if not answer.isdigit() and not answer.lstrip('-').isdigit():
                print("Please enter a valid numerical input.\n")
                continue

            answerAsInt = int(answer) - 1
            if answerAsInt < 0:
                print("Page number must be positive.\n")
                continue

            pid = str(answerAsInt)

        nextPid = pid
        while nextPid.lower() != 'new':
            batches = getPosts(limit, tags, int(nextPid), selectedRatings)
        
            for selected in selectedRatings:
            
                yesOrNo = ''

                while yesOrNo == '':
                    answer = input(f"\nWould you like to download rating:{selected} images? (y / n, yes / no, 1 / 0)\n>>> ").lower().strip()
                
                    if answer not in acceptableAnswersY and answer not in acceptableAnswersN:
                        print("Please select a valid answer.\n")
                        continue

                    yesOrNo = answer
            
                if yesOrNo in acceptableAnswersY:
                    response = batches[selected]

                    if '@attributes' not in response or 'post' not in response:
                        print(f"\nNo images were found for rating:{selected}.")
                        continue
                
                    for post in response['post']:
                        print(f"\nDownloading {post['image']} to img/{selected}...")
                        with open(f'img/{selected}/' + post['image'], 'wb') as imageWriter:
                            img = requests.get(post['file_url'], stream = True)
                            for chunk in img.iter_content(1024):
                                if not chunk: break
                                imageWriter.write(chunk)
            
            print()
            for selected in selectedRatings:
                count = batches[selected]['@attributes']['count']
                print(f"rating:{selected} - Currently on page {int(nextPid) + 1}/{count if count // limit == count else count // limit + 1}")

            temp = ''
            while temp != 'new' and not temp.isdigit():
                answer = input(f"\nPlease enter a page number to go to, or 'new' to start over.\n>>> ")
                
                if answer == 'new': 
                    temp = answer
                    break

                if not answer.isdigit() and not answer.lstrip('-').isdigit():
                    print("Please enter a valid numerical input.\n")
                    continue

                answerAsInt = int(answer) - 1
                if answerAsInt < 0:
                    print("Page number must be positive.\n")
                    continue

                temp = str(answerAsInt)

            nextPid = temp.lower()

if __name__ == "__main__":
    main()
