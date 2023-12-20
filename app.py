
import random

# test edit
def makePrefixDict(wordList):
    prefixDict = {}
    for word in wordList:
        for i in range(1, len(word)):  
            prefixDict[word[0:i]] = 1
    return prefixDict


def indexExists(row, col):
    if row > 3 or row < 0 or col > 3 or col < 0:
        return False
    else:
        return True


def comboIsWord(combo, wordList):
    if combo in wordList:
        return True
    else:
        return False
    

def comboIsPrefix(combo, prefixDict):
    if combo in prefixDict:
        return True
    else:
        return False


def generateBoard():
    dice = [['A', 'A', 'E', 'E', 'G', 'N'],
            ['A', 'O', 'O', 'T', 'T', 'W'],
            ['D', 'I', 'S', 'T', 'T', 'Y'],
            ['E', 'I', 'O', 'S', 'S', 'T'],
            ['A', 'B', 'B', 'J', 'O', 'O'],
            ['C', 'I', 'M', 'O', 'T', 'U'],
            ['E', 'E', 'G', 'H', 'N', 'W'],
            ['E', 'L', 'R', 'T', 'T', 'Y'],
            ['A', 'C', 'H', 'O', 'P', 'S'],
            ['D', 'E', 'I', 'L', 'R', 'X'],
            ['E', 'E', 'I', 'N', 'S', 'U'],
            ['H', 'I', 'M', 'N', 'Q', 'U'],
            ['A', 'F', 'F', 'K', 'P', 'S'],
            ['D', 'E', 'L', 'R', 'V', 'Y'],
            ['E', 'H', 'R', 'T', 'V', 'W'],
            ['H', 'L', 'N', 'N', 'R', 'Z']]
    
    board = [[None for y in range(4)]for x in range(4)]

    lettersInBoard = []
    for item in dice:
        random.shuffle(item)
        lettersInBoard.append(item[0])
        random.shuffle(lettersInBoard)
        
    k = 0
    for i in range(4):
        for j in range(4):
            board[i][j] = lettersInBoard[k]
            k += 1

    return board


def validate_input(letters):
    # Split the input into rows
    rows = letters.strip().split('\n')

    # Check if there are exactly 4 rows
    if len(rows) != 4:
        return False

    # Check if each row has exactly 4 letters and each letter is valid
    for row in rows:
        if len(row.strip()) != 4 or not all(char.isalpha() for char in row.strip()):
            return False

    # If all checks pass, the input is valid
    return True



    

def searchForWords(board, row, col, wordsFound, prefixDict, combo, wordList, nodesVisited, minLength, nodesInWord):
    circle = [ [(row-1),(col)],
               [(row-1),(col+1)],
               [(row),(col+1)],
               [(row+1),(col+1)],
               [(row+1),(col)] ,
               [(row+1),(col-1)],
               [(row),(col-1)],
               [(row-1),(col-1)] ]
    
   
    for node in circle:  
        
        if node not in nodesVisited and indexExists(node[0], node[1]):
            
            potential_combo = combo + board[node[0]][node[1]]   # add node in circle to the current combo

            if comboIsWord(potential_combo, wordList) and potential_combo not in wordsFound.keys() and len(potential_combo) >= minLength:
                # wordsFound.append(potential_combo)
                
                nodesInWord = nodesVisited.copy()
                nodesInWord.append(node)
                wordsFound[potential_combo] = nodesInWord
                

            if comboIsPrefix(potential_combo, prefixDict):
                nodesVisited.append(node)
                searchForWords(board, node[0], node[1], wordsFound, prefixDict, potential_combo, wordList, nodesVisited, minLength, nodesInWord)
            else:
                potential_combo = combo
                next

    nodesVisited.pop()
    # if len(nodesInWord) > 0:
    #     nodesInWord.pop()
    


def main(board=None, minLength=3, boardType='R'):

    dictionaryOG = open('words.txt').read().split()
    wordList = {}
    for item in dictionaryOG:
        wordList[item.upper()] = 1
        
    prefixDict = makePrefixDict(wordList)

    # wordsFound = []


    wordsFound = {}

    if board == None:
        board = generateBoard()

    for row in range(0, len(board)):
        for col in range(0, len(board[0])):
            nodesVisited = [[row, col]]
            combo = board[row][col]
            nodesInWord = [[row, col]]
            searchForWords(board, row, col, wordsFound, prefixDict, combo, wordList, nodesVisited, minLength, nodesInWord)

    return wordsFound


main()


from flask import Flask, render_template, request, jsonify, flash

app = Flask(__name__)
app.secret_key = 'JERbi121698!'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def index2():
    return render_template('index.html')

@app.route('/boggle.html')
def boggle_home():
    return render_template('boggle.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/myprojects.html')
def projects():
    return render_template('myprojects.html')


@app.route('/solve_boggle', methods=['POST'])
def solve_boggle():

    # Initialize board before the try block
    board = None
    words_found = None

    try:
        # Extract data from the form
        board_type = request.form.get('board_type')
        min_length = int(request.form.get('min_length'))

        # Call your Boggle solver function
        if board_type == 'R':
            letters = request.form.get('input_board')
            
            board = generateBoard()
            words_found = main(board, min_length, board_type)
        else:
            letters = request.form.get('input_board')

            # Validate the user input
            if not validate_input(letters):
                # Handle invalid input (e.g., flash an error message)
                flash("Invalid input. Please enter exactly 16 valid letters, with 4 letters on 4 rows.")
            else:
                # Initialize the board
                board = []

                for row in letters.upper().split('\n'):
                    row = list(row.strip())
                    board.append(row)

                words_found = main(board, min_length, board_type)

    except ValueError as e:
        flash(str(e))
        # Handle other exceptions if needed
        # ...

    # Pass the result to the template
    # if 'letters' in locals():
    #     return render_template('boggle.html', words_found=words_found, board=board, letters=letters)
    # else:
    #     return render_template('boggle.html', words_found=words_found, board=board)

    return render_template('boggle.html', words_found=words_found, board=board, letters=letters, min_length=min_length)



if __name__ == '__main__':
    app.run(debug=True)

