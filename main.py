import random
# import os
import katagames_sdk as katasdk

kataen = katasdk.engine
pygame = kataen.import_pygame()

# - - CONSTANTS - -
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

X_CST = 344
X_OFFSET = 80

# we declare various game states
MENU_GS, TUTORIAL_GS, PAUSE_GS, PLAY_GS = range(4)  # one code per gamestate(GS)

# - - global variables - -
curr_gs = MENU_GS  # current game state

playerScoreadd = False
computerScoreadd = False
playerScore = 0
computerScore = 0
playerScoreList = []
computerScoreList = []
score_value = []
gameover = False
menus = True
highscore = False
tutorial = False
pause = False
choice = ['rock', 'paper', 'scissor']
playerList = []
computerList = []
randElement = random.choice(choice)
computerList.append(randElement)

win = pygame.Surface((0, 0))
display = [0, 0]  # size


@katasdk.web_entry_point
def init_game():
    global win, display
    kataen.init()
    win = kataen.get_screen()  # instead of: pygame.display.set_mode(display)
    display[0], display[1] = win.get_size()


def message_to_screen2center(font, size, text, color, pos):
    font = pygame.font.SysFont(font, size)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.center = pos
    win.blit(text, textRect)


def score(playerscore, compscore, playeradd, compadd):
    if playeradd:
        playerscore += 1
    if compadd:
        compscore += 1
    message_to_screen2center('lucidaconsole', 20, playerscore, black, (display[0] // 2, (display[1] // 2) - 10))
    message_to_screen2center('lucidaconsole', 20, compscore, black, (display[0] // 2, (display[1] // 2) + 10))


def savscore(winner, loser):
    print('saving highscore')
    a = open('score.txt', 'w')
    a.write(str(winner)+':'+str(loser)+', ')
    a.close()


def highscorecheck(winner, loser):
    # TODO add comments to describe the logic behind this function
    # TODO fix bugs if score > 10
    b = open('highscore.txt', 'r')
    text = b.read()
    b.close()
    text = str(text)
    textSplit = text.split(':')
    wins = int(textSplit[0])
    loses = int(textSplit[1])
    score1 = wins - loses
    score2 = winner - loser
    if score1 < score2:
        c = open('highscore.txt', 'w')
        c.write(str(winner)+':'+str(loser))
    if score1 == score2:
        if wins < winner:
            c.write('highscore.txt')
            c.write(str(winner)+':'+str(loser))
        if wins > winner:
            c.write('highscore.txt')
            c.write(str(wins)+':'+str(loses))


# utility function
def img(name):
    # local
    if not kataen.runs_in_web():
        import os
        return pygame.image.load(os.sep.join(('assets', name+'.png')))
    # web-compatible
    return pygame.image.load(name + '.png')


def update_menu_gs():
    global play_btnRect, how_to_playRect, gameover, curr_gs  # define global variables (defined not locally)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            playstartx = play_btnRect[0]
            playendx = play_btnRect[0] + play_btnRect[2]
            playstarty = play_btnRect[1]
            playendy = play_btnRect[1] + play_btnRect[3]
            tutorialstartx = how_to_playRect[0]
            tutorialendx = how_to_playRect[0] + how_to_playRect[2]
            tutorialstarty = how_to_playRect[1]
            tutorialendy = how_to_playRect[1] + how_to_playRect[3]
            if pos[0] >= playstartx and pos[0] < playendx and pos[1] > playstarty and pos[1] < playendy:
                curr_gs = PLAY_GS
            if pos[0] >= tutorialstartx and pos[0] < tutorialendx and pos[1] > tutorialstarty and pos[1] < tutorialendy:
                curr_gs = TUTORIAL_GS
    
    win.fill(yellow)
    c = open('highscore.txt', 'r')
    text = c.read()
    c.close
    title = img('title')
    title = pygame.transform.scale(title, (47 * 14, 21 * 14))
    titleRect = title.get_rect()
    titleRect.center = ((display[0] // 2), (display[1] // 2) - 150)
    win.blit(title, titleRect)
    play_btn = img('play')
    play_btn = pygame.transform.scale(play_btn, (4 * 50, 1 * 50))
    play_btnRect = play_btn.get_rect()
    play_btnRect.center = ((display[0] // 2), ((display[1] // 2) + 50))
    win.blit(play_btn, play_btnRect)
    highscore = img('highscore')
    highscore = pygame.transform.scale(highscore, (80 * 5, 9 * 5))
    highscoreRect = highscore.get_rect()
    highscoreRect.center = ((display[0] // 2), (display[1] // 2) + 103)
    win.blit(highscore, highscoreRect)
    how_to_play = img('how_to_play')
    how_to_play = pygame.transform.scale(how_to_play, (12 * 17, 7 * 17))
    how_to_playRect = how_to_play.get_rect()
    how_to_playRect.center = ((display[0] // 2), (display[1] // 2) + 190)
    win.blit(how_to_play, how_to_playRect)
    message_to_screen2center('lucidaconsole', 30, str(text), black, ((display[0] // 2) + 140, (display[1] // 2) + 104))


def update_tutorial_gs():
    global gameover, menus, backbtnRect, curr_gs
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            backbtnstartx = backbtnRect[0]
            backbtnendx = backbtnRect[0] + backbtnRect[2]
            backbtnstarty = backbtnRect[1]
            backbtnendy = backbtnRect[1] + backbtnRect[3]
            if pos[0] >= backbtnstartx and pos[0] <= backbtnendx and pos[1] >= backbtnstarty and pos[1] <= backbtnendy:
                curr_gs = MENU_GS
    
    win.fill(yellow)
    backbtn = img('back')
    backbtn = pygame.transform.scale(backbtn, (36 * 5, 9 * 5))
    backbtnRect = backbtn.get_rect()
    backbtnRect.center = (display[0] // 2, display[1] // 2)
    win.blit(backbtn, backbtnRect)
    message_to_screen2center("lucidaconsole", 20, "1)Use the buttons in the game screen to select rock, paper, scissors.", black, (display[0] // 2, 56))
    message_to_screen2center("lucidaconsole", 20, "2)While using save score button this game checks whether it is a ", black, (display[0] // 2, 86))
    message_to_screen2center("lucidaconsole", 20, "highscore or not and save it respectively.", black, (display[0] // 2, 116))
    message_to_screen2center("lucidaconsole", 20, "4)If you want to see the score with opening the game then you can ", black, (display[0] // 2, 146))
    message_to_screen2center("lucidaconsole", 20, "find a file named score.txt in your device for fing=ding all the scores ", black, (display[0] // 2, 176))
    message_to_screen2center("lucidaconsole", 20, "or the highscore.txt file for the highscore.", black, (display[0] // 2, 206))
    message_to_screen2center("lucidaconsole", 20, "5)You can click on the back button in the paused menu to go to the menus.", black, (display[0] // 2, 236))


def update_pause_gs():
    global gameover, resumeRect, backRect, curr_gs
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            resumestartx = resumeRect[0]
            resumendx = resumeRect[0] + resumeRect[2]
            resumestarty = resumeRect[1]
            resumendy = resumeRect[1] + resumeRect[3]
            backstartx = backRect[0]
            backendx = backRect[0] + backRect[2]
            backstarty = backRect[1]
            backendy = backRect[1] + backRect[3]
            if pos[0] >= resumestartx and pos[0] <= resumendx and pos[1] >= resumestarty and pos[1] <= resumendy:
                curr_gs = PLAY_GS
            if pos[0] >= backstartx and pos[0] <= backendx and pos[1] >= backstarty and pos[1] <= backendy:
                playerscore = compscore = 0
                playerList.clear()
                computerList.clear()
                randElement = random.choice(choice)
                curr_gs = MENU_GS

    win.fill((100, 100, 100))
    label = img('paused')
    label = pygame.transform.scale(label, (14 * 18, 3 * 19))
    labelRect = label.get_rect()
    labelRect.center = (display[0] // 2, 110)
    pygame.draw.rect(win, ((50, 50, 50)), (labelRect[0] - 10, labelRect[1] - 10, labelRect[2] + 20, 180))
    win.blit(label, labelRect)
    resume = img('resume')
    resume = pygame.transform.scale(resume, (14 * 14, 3 * 14))
    resumeRect = resume.get_rect()
    resumeRect.center = (display[0] // 2, 170)
    win.blit(resume, resumeRect)
    back = img('back')
    back = pygame.transform.scale(back, (36 * 5, 9 * 5))
    backRect = back.get_rect()
    backRect.center = (display[0] // 2, (display[1] // 2) - 80)
    win.blit(back, backRect)


def update_play_gs():
    global menus, gameover, playendx, playerScore, computerScore, curr_gs
    global playagainRect, pausebtnRect, savescoreRect, randElement
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos  # use position given by the event
            playagainstartx = playagainRect[0]
            playagainendx = playagainRect[0] + playagainRect[2]
            playagainstarty = playagainRect[1]
            playagainendy = playagainRect[1] + playagainRect[3]
            pausestartx = pausebtnRect[0]
            pausendx = pausebtnRect[0] + pausebtnRect[2]
            pausestarty = pausebtnRect[1]
            pausendy = pausebtnRect[1] + pausebtnRect[3]
            savestartx = savescoreRect[0]
            savendx = savescoreRect[0] + savescoreRect[2]
            savestarty = savescoreRect[1]
            savendy = savescoreRect[1] + savescoreRect[3]
            if pos[0] >= ((X_CST // 2) - 100) - 40 and pos[0] <= ((X_CST // 2) - 100) + 40 and pos[1] >= (display[1] - 60) - 40 and pos[1]  <= (display[1] - 60) + 50:
                playerList.append('rock')
                playerScoreList.append(playerList)
                computerList.append(randElement)
                computerScoreList.append(computerList)
            if pos[0] >= (X_CST // 2) - 40 and pos[0] <= (X_CST // 2) + 40 and pos[1] >= (display[1] - 60) - 40 and pos[1]  <= (display[1] - 60) + 50:
                playerList.append('paper')
                playerScoreList.append(playerList)
                computerList.append(randElement)
                computerScoreList.append(computerList)
            if pos[0] >= ((X_CST // 2) + 100) - 40 and pos[0] <= ((X_CST // 2) + 100) + 40 and pos[1] >= (display[1] - 60) - 40 and pos[1]  <= (display[1] - 60) + 50:
                playerList.append('scissor')
                playerScoreList.append(playerList)
                computerList.append(randElement)
                computerScoreList.append(computerList)
            if pos[0] >= playagainstartx and pos[0] <= playagainendx and pos[1] >= playagainstarty and pos[1] <= playagainendy:
                playerList.clear()
                computerList.clear()
                playerScoreList.clear()
                computerScoreList.clear()
                randElement = random.choice(choice)
            if pos[0] >= pausestartx and pos[0] <= pausendx and pos[1] >= pausestarty and pos[1] <= pausendy:
                curr_gs = PAUSE_GS
            if pos[0] >= savestartx and pos[0] <= savendx and pos[1] >= savestarty and pos[1] <= savendy:
                savscore(playerScore, computerScore)
                highscorecheck(playerScore, computerScore)

    win.fill(black)
    pygame.draw.rect(win, yellow, (10, 10, X_CST, display[1] - 20))
    pygame.draw.rect(win, yellow, (364, 10, 172, display[1] - 20))
    pygame.draw.rect(win, yellow, (546, 10, X_CST, display[1] - 20))
    savescore = img('saveScore')
    savescore = pygame.transform.scale(savescore, (12 * 14, 5 * 14))
    savescoreRect = savescore.get_rect()
    savescoreRect.center = (display[0] // 2, display[1] - 70)
    win.blit(savescore, savescoreRect)
    playagain = img('playAgain')
    playagain = pygame.transform.scale(playagain, (12 * 14, 5 * 14))
    playagainRect = playagain.get_rect()
    playagainRect.center = (display[0] // 2, display[1] - 160)
    win.blit(playagain, playagainRect)
    pausebtn = img('pause')
    pausebtn = pygame.transform.scale(pausebtn, (4 * 42, 1 * 42))
    pausebtnRect = pausebtn.get_rect()
    pausebtnRect.center = (display[0] // 2, display[1] - 237)
    win.blit(pausebtn, pausebtnRect)
    btn = img('button')
    btnscale = (90, 90)
    scorebanner = img('score')
    scorebanner = pygame.transform.scale(scorebanner, (4 * 42, 1 * 42))
    scorebannerRect = scorebanner.get_rect()
    scorebannerRect.center = (display[0] // 2, (display[1] // 2) - 100)
    win.blit(scorebanner, scorebannerRect)
    btn1 = pygame.transform.scale(btn, btnscale)
    btn1Rect = btn1.get_rect()
    btn1Rect.center = ((X_CST // 2) - X_OFFSET, display[1] - 60)
    win.blit(btn1, btn1Rect)
    btn2 = pygame.transform.scale(btn, btnscale)
    btn2Rect = btn2.get_rect()
    btn2Rect.center = ((X_CST // 2), display[1] - 60)
    win.blit(btn2, btn2Rect)
    btn3 = pygame.transform.scale(btn, btnscale)
    btn3Rect = btn3.get_rect()
    btn3Rect.center = ((X_CST // 2) + X_OFFSET, display[1] - 60)
    win.blit(btn3, btn3Rect)
    rock = img('ROCK')
    paper = img('PAPER')
    scissor = img('SCISSOR')
    rock = pygame.transform.scale(rock, (7 * 7, 9 * 7))
    paper = pygame.transform.scale(paper, (14 * 3, 23 * 3))
    scissor = pygame.transform.scale(scissor, (5 * 8, 8 * 8))
    rockRect = rock.get_rect()
    paperRect = paper.get_rect()
    scissorRect = paper.get_rect()
    rockRect.center = ((X_CST // 2) - 100, display[1] - 60)
    paperRect.center = (X_CST // 2, display[1] - 60)
    scissorRect.center = ((X_CST // 2) + 100, display[1] - 60)
    win.blit(rock, rockRect)
    win.blit(paper, paperRect)
    win.blit(scissor, scissorRect)
    if len(playerList) > 0:
        if playerList[0] == choice[0]:
            rock = img('ROCK')
            rock = pygame.transform.scale(rock, (7 * 32, 9 * 32))
            rock = pygame.transform.rotate(rock, -90)
            rockRect = rock.get_rect()
            rockRect.center = (X_CST // 2, display[1] // 2)
            win.blit(rock, rockRect)
        if playerList[0] == choice[1]:
            paper = img('PAPER')
            paper = pygame.transform.scale(paper, (14 * 12, 23 * 12))
            paper = pygame.transform.rotate(paper, -90)
            paperRect = paper.get_rect()
            paperRect.center = (X_CST // 2, display[1] // 2)
            win.blit(paper, paperRect)
        if playerList[0] == choice[2]:
            scissor = img('SCISSOR')
            scissor = pygame.transform.scale(scissor, (5 * 37, 8 * 37))
            scissor = pygame.transform.rotate(scissor, -90)
            scissorRect = scissor.get_rect()
            scissorRect.center = (X_CST // 2, display[1] // 2)
            win.blit(scissor, scissorRect)
        if computerList[0] == choice[0]:
            rock = img('ROCK')
            rock = pygame.transform.scale(rock, (7 * 32, 9 * 32))
            rock = pygame.transform.rotate(rock, 90)
            rockRect = rock.get_rect()
            rockRect.center = (546 + 172, display[1] // 2)
            win.blit(rock, rockRect)
        if computerList[0] == choice[1]:
            paper = img('PAPER')
            paper = pygame.transform.scale(paper, (14 * 12, 23 * 12))
            paper = pygame.transform.rotate(paper, 90)
            paperRect = paper.get_rect()
            paperRect.center = (546 + 172, display[1] // 2)
            win.blit(paper, paperRect)
        if computerList[0] == choice[2]:
            scissor = img('SCISSOR')
            scissor = pygame.transform.scale(scissor, (5 * 37, 8 * 37))
            scissor = pygame.transform.rotate(scissor, 90)
            scissorRect = scissor.get_rect()
            scissorRect.center = (546 + 172, display[1] // 2)
            win.blit(scissor, scissorRect)

        if playerList[0] == computerList[0]:
            tie = img('tie')
            tie = pygame.transform.scale(tie, (14 * 10, 5 * 10))
            tieRect = tie.get_rect()
            tieRect.center = (display[0] // 2, 50)
            win.blit(tie, tieRect)
        elif playerList[0] == 'rock':
            if computerList[0] == 'paper':
                winner = img('winner')
                winner = pygame.transform.scale(winner, (35 * 8, 5 * 8))
                winnerRect = winner.get_rect()
                winnerRect.center = (546 + 172, 50)
                win.blit(winner, winnerRect)
                loser = img('loser')
                loser = pygame.transform.scale(loser, (24 * 8, 5 * 8))
                loserRect = loser.get_rect()
                loserRect.center = (X_CST // 2, 50)
                win.blit(loser, loserRect)
                if len(computerScoreList) > 0:
                    computerScore += 1
                    computerScoreList.clear()
            elif computerList[0] == 'scissor':
                winner = img('winner')
                winner = pygame.transform.scale(winner, (35 * 8, 5 * 8))
                winnerRect = winner.get_rect()
                winnerRect.center = (X_CST // 2, 50)
                win.blit(winner, winnerRect)
                loser = img('loser')
                loser = pygame.transform.scale(loser, (24 * 8, 5 * 8))
                loserRect = loser.get_rect()
                loserRect.center = (546 + 172, 50)
                win.blit(loser, loserRect)
                if len(playerScoreList) > 0:
                    playerScore += 1
                    playerScoreList.clear()
        elif playerList[0] == 'paper':
            if computerList[0] == 'rock':
                winner = img('winner')
                winner = pygame.transform.scale(winner, (35 * 8, 5 * 8))
                winnerRect = winner.get_rect()
                winnerRect.center = (X_CST // 2, 50)
                win.blit(winner, winnerRect)
                loser = img('loser')
                loser = pygame.transform.scale(loser, (24 * 8, 5 * 8))
                loserRect = loser.get_rect()
                loserRect.center = (546 + 172, 50)
                win.blit(loser, loserRect)
                if len(playerScoreList) > 0:
                    playerScore += 1
                    playerScoreList.clear()
            elif computerList[0] == 'scissor':
                winner = img('winner')
                winner = pygame.transform.scale(winner, (35 * 8, 5 * 8))
                winnerRect = winner.get_rect()
                winnerRect.center = (546 + 172, 50)
                win.blit(winner, winnerRect)
                loser = img('loser')
                loser = pygame.transform.scale(loser, (24 * 8, 5 * 8))
                loserRect = loser.get_rect()
                loserRect.center = (X_CST // 2, 50)
                win.blit(loser, loserRect)
                if len(computerScoreList) > 0:
                    computerScore += 1
                    computerScoreList.clear()
        elif playerList[0] == 'scissor':
            if computerList[0] == 'paper':
                winner = img('winner')
                winner = pygame.transform.scale(winner, (35 * 8, 5 * 8))
                winnerRect = winner.get_rect()
                winnerRect.center = (X_CST // 2, 50)
                win.blit(winner, winnerRect)
                loser = img('loser')
                loser = pygame.transform.scale(loser, (24 * 8, 5 * 8))
                loserRect = loser.get_rect()
                loserRect.center = (546 + 172, 50)
                win.blit(loser, loserRect)
                if len(playerScoreList) > 0:
                    playerScore += 1
                    playerScoreList.clear()
            elif computerList[0] == 'rock':
                winner = img('winner')
                winner = pygame.transform.scale(winner, (35 * 8, 5 * 8))
                winnerRect = winner.get_rect()
                winnerRect.center = (546 + 172, 50)
                win.blit(winner, winnerRect)
                loser = img('loser')
                loser = pygame.transform.scale(loser, (24 * 8, 5 * 8))
                loserRect = loser.get_rect()
                loserRect.center = (X_CST // 2, 50)
                win.blit(loser, loserRect)
                if len(computerScoreList) > 0:
                    computerScore += 1
                    computerScoreList.clear()
    message_to_screen2center('lucidaconsole', 90, str(playerScore)+':'+str(computerScore), black, ((display[0] // 2), (display[1] // 2) - 20))


# - associative structure: gamestate code to update function
assoc_gs_to_updatefunc = {
    MENU_GS: update_menu_gs,
    TUTORIAL_GS: update_tutorial_gs,
    PAUSE_GS: update_pause_gs,
    PLAY_GS: update_play_gs
}


@katasdk.web_animate
def generic_update():
    adhoc_func = assoc_gs_to_updatefunc[curr_gs]
    adhoc_func()
    kataen.display_update()


if __name__ == '__main__':
    init_game()
    while not gameover:
        generic_update()

    print(playerScore)
    print(computerScore)
    kataen.cleanup()
