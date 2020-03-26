#word
punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']

def strip_punctuation(word):
    for char in punctuation_chars:
        if char in word:
            word=word.replace(char,'')
    return(word)

# list of positive words to use
positive_words = []
with open("positive_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            positive_words.append(lin.strip())

# positive count
def get_pos(sentence):
    n=0
    sentence=strip_punctuation(sentence)
    for word in sentence.split():
        word=word.lower()
        if word in positive_words:
            n=n+1
    return n

# list of negative words to use
negative_words = []
with open("negative_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            negative_words.append(lin.strip())

# negative count
def get_neg(sentence):
    m=0
    sentence=strip_punctuation(sentence)
    for word in sentence.split():
        word=word.lower()
        if word in negative_words:
            m=m+1
    return m

# open the file
with open('project_twitter_data.csv','r') as origin:
    lines = origin.readlines()
    contents=[]
    retweets=[]
    replies=[]
    for line in lines[1:]:
        vals=line.strip().split(',')
        contents.append(vals[0])
        retweets.append(vals[1])
        replies.append(vals[2])

# score
pos_score=[]
neg_score=[]
net_score=[]
for content in contents:
    pos_score.append(get_pos(content))
    neg_score.append(get_neg(content))
    net_score.append(get_pos(content)-get_neg(content))

# write the file
with open('resulting_data.csv','w') as new:
    new.write('Number of Retweets, Number of Replies, Positive Score, Negative Socre, Net Score')
    new.write('\n')
    n=0
    for row in lines[1:]:
        row_string='{},{},{},{},{}'.format(retweets[n],replies[n],pos_score[n],neg_score[n],net_score[n])
        new.write(row_string)
        new.write('\n')
        n=n+1
