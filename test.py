# import time
# from doctest import master
#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
#
# driver = webdriver.Chrome()
#
# master = ["Bram Stoker's Dracula", 'Blink Twice', 'A Nightmare on Elm Street', 'Am I Racist?', 'The Brutalist', 'The Rocky Horror Picture Show', 'Ghostbusters: Frozen Empire', 'Inside Out 2', 'Scream', 'Wolfs', 'Megalopolis', 'The Shining', 'Subservience', 'The Addams Family', 'Nosferatu', 'Hocus Pocus 2', 'Pearl', 'Interstellar', 'Scary Movie', 'Twisters', 'Practical Magic', "Harry Potter and the Sorcerer's Stone", 'The Shawshank Redemption', 'Halloween', 'Casper', 'Stree 2: Sarkate Ka Aatank', 'Azrael', 'Babygirl', 'The Room Next Door', 'Joker', 'Coraline', 'Challengers', 'Oddity', 'Hereditary', 'The Shadow Strays', 'Saturday Night', 'Civil War', 'Sleepy Hollow', 'Maria', 'Scream VI', 'Small Things Like These', 'Ghostbusters', "All Hallows' Eve"]
#
#
# driver.get('https://movieportfolio.onrender.com/')
#
# for movie in master:
#     addmovie = driver.find_element(By.XPATH, '/html/body/header/ul/li[4]/a')
#     addmovie.click()
#     titlem = driver.find_element(By.ID, 'title')
#     titlem.click()
#     titlem.send_keys(movie)
#     subm = driver.find_element(By.ID, 'submit')
#     subm.click()
#     try:
#         selected = driver.find_element(By.CLASS_NAME, 'searchtitle')
#         selected.click()
#     except:
#         driver.back()
#         addmovie = driver.find_element(By.XPATH, '/html/body/header/ul/li[4]/a')
#         addmovie.click()
#
#
#
#
#
#
# # user_name = driver.find_element(By.CLASS_NAME, "_aa48")
# # user_name.click()
# # user_name.send_keys(user_id)
# # user_name.send_keys(Keys.TAB, password_id)
# # user_name.send_keys(Keys.ENTER)
# # time.sleep(5)
#
#
#
# # master = ['Venom: The Last Dance', 'The Substance', "Don't Move", 'Terrifier 3', 'Woman of the Hour', 'Trap', 'Joker: Folie à Deux', 'The Wild Robot', 'Smile 2', 'Anora', 'Gladiator II', 'Beetlejuice Beetlejuice', 'Terrifier', 'Beetlejuice', 'Time Cut', 'Queer', 'Hocus Pocus', 'Heretic', 'Alien: Romulus', 'Terrifier 2', 'Here', 'Do Patti', 'Conclave', 'Deadpool & Wolverine', 'Canary Black', 'The Apprentice', 'Longlegs', 'We Live in Time', 'Halloween', 'Caddo Lake', 'X', 'Smile', 'Transformers One', 'Scream', 'Wicked', 'MaXXXine', 'Juror #2', 'The Nightmare Before Christmas', 'Apocalypse Z: The Beginning of the End', 'Late Night with the Devil', 'Speak No Evil', 'The Batman', "Trick 'r Treat", 'The Remarkable Life of Ibelin', 'Venom', 'Red One', "It's What's Inside", 'Strange Darling', 'Young Frankenstein', 'Brothers', "Salem's Lot", 'Lee', 'Venom: Let There Be Carnage', 'It Ends with Us', 'Gladiator', 'Family Pack', 'It', "Bram Stoker's Dracula", 'Blink Twice', 'A Nightmare on Elm Street', 'Am I Racist?', 'The Brutalist', 'The Rocky Horror Picture Show', 'Ghostbusters: Frozen Empire', 'Inside Out 2', 'Scream', 'Wolfs', 'Megalopolis', 'The Shining', 'Subservience', 'The Addams Family', 'Nosferatu', 'Hocus Pocus 2', 'Pearl', 'Interstellar', 'Scary Movie', 'Twisters', 'Practical Magic', "Harry Potter and the Sorcerer's Stone", 'The Shawshank Redemption', 'Halloween', 'Casper', 'Stree 2: Sarkate Ka Aatank', 'Azrael', 'Babygirl', 'The Room Next Door', 'Joker', 'Coraline', 'Challengers', 'Oddity', 'Hereditary', 'The Shadow Strays', 'Saturday Night', 'Civil War', 'Sleepy Hollow', 'Maria', 'Scream VI', 'Small Things Like These', 'Ghostbusters', "All Hallows' Eve"]
# # print(len(master))
# # # Set up the webdriver (make sure ChromeDriver is in your PATH)
# # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# #
# # # Fetch the webpage
# # url = 'https://movieportfolio.onrender.com/'
# # driver.get(url)
# #
# # # Wait for the page to load (you can add more time if needed)
# # driver.implicitly_wait(10)
# #
# #
# #
# #
# # # Get the page source and parse with BeautifulSoup
# # soup = BeautifulSoup(driver.page_source, 'html.parser')
# #
# # # Find all <h3> tags
# # data = [h3.get_text(strip=True) for h3 in soup.find_all('h3')]
# #
# # # Print the result
# # print(data)
#
# # Close the browser
# driver.quit()


