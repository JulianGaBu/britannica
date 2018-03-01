# -*- coding: utf-8 -*-
from lxml import etree
from pyscraper.iterator import _gen_tree

tree = _gen_tree('https://www.britannica.com/topic/list-of-cities-and-towns-in-the-United-States-2023068')
links = tree.xpath('//a[@class="md-crosslink"]')

def getloc(symbol, location_state, word_list):
    if symbol in location_state:
        for chunk in location_state.split(symbol):
            if any(word in chunk.lower() for word in word_list):
                return chunk.strip()
        else:
            print('wait, what? no state location?', 'symbol')
    else:
        return location_state

def getallloc(text, word_list):
    string = text
    string = getloc('[', string, word_list)
    string = getloc(']', string, word_list)
    string = getloc('(', string, word_list)
    string = getloc(')', string, word_list)
    string = getloc(';', string, word_list)
    return string
# def recursive_shit(element):
#     children = element.getchildren()
#     if len(children) < 1:
#         head = (element.text + ' ') if element.text is not None else ''
#         tail = (element.tail + ' ') if element.tail is not None else ''
#         return head + tail + ' '
#     return ''.join([recursive_shit(child) for child in children])
#
#
# def stringify_children(node):
#     from lxml.etree import tostring
#     from itertools import chain
#     parts = ([node.text] +
#              list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren()))) +
#              [node.tail])
#     # filter removes possible Nones in texts and tails
#     return ''.join(filter(None, parts))
#
# def chtm(node):
#     return ''.join(node.itertext())


# def get_text(elements):
#     final_string = ''
#     if isinstance(elements, list):
#         for element in elements:
#             children = element.getchildren()
#             text = element.text.strip() + ' ' if element.text is not None else ''
#             if element.tag == 'a':
#                 attr = element.get('href')
#                 root = 'https://www.mass.gov' if attr[0] == '/' else ''
#                 if root == '': print '\nEMPTY LINK NIGGUUUUUH\n'
#                 if 'tel:' not in attr and 'mailto:' not in attr:
#                     link = '(' + root + attr + ')'
#                     print link
#                 else:
#                     link = ''
#             else:
#                 link = ''
#             # link = ('(' + element.get_attribute('href') + ')') if element.tag == 'a' else ''
#             tail = element.tail.strip() + ' ' if element.tail is not None else ''
#             final_string += text + link + tail + '\n'
#             if len(children) > 0:
#                 final_string += get_text(children)
#     else:
#         element = elements
#         children = element.getchildren()
#         if len(children) > 0:
#             final_string += get_text(children)
#         else:
#             final_string += ((element.text.strip() + '\n') if element.text is not None else '') + ((element.tail.strip() + '\n') if element.tail is not None else '') + '\n'
#     return final_string.strip()

# for link in links:
#     print recursive_shit(link)
with open('owo.txt', 'a+') as output:
    for link in [link.get('href') for link in links[4:]]:
        try:
            tree = _gen_tree(link)
            # paragraph = recursive_shit(tree.xpath('//article[@class="content"]')[0])
            paragraph = ''.join(tree.xpath('//article[@class="content"]')[0].itertext())
            state = tree.xpath('//*[@id="content"]/main/div[1]')[0].text.split(',')  # [0].strip()
            if 'state' in state[0].strip() or state[0].strip() is 'town':
                continue
            elif any(word in state[0].strip() for word in ['historical', 'district', 'capital', 'pueblo', 'county', 'city', 'resort', 'settlement', 'borough', 'township', 'amusement', 'village']):
                state = state[1]
            else:
                state = state[0]
            if len(state) > 50:
                print('skipped')
                continue

            # print('wut state')
            # recursive_shit(paragraph)
            # name = paragraph.xpath('//strong.text()')
            # text = paragraph.text
            paragraphs = paragraph.split(',')
            index = 0
            name = paragraphs[index].strip()
            index += 1
            for i in range(index, len(paragraphs)):
                if 'city' in paragraphs[i].strip().lower():
                    city_or_town = 'City'
                elif 'town' in paragraphs[i].strip().lower():
                    city_or_town = 'Town'
                elif 'township' in paragraphs[i].strip().lower():
                    city_or_town = 'Township'
                elif 'village' in paragraphs[i].strip().lower():
                    city_or_town = 'Village'
                elif 'reservation' in paragraphs[i].strip().lower():
                    city_or_town = 'Reservation'
                elif 'capital' in paragraphs[i].strip().lower():
                    city_or_town = 'Capital'
                if any(word in paragraphs[i].strip().lower() for word in ['city', 'village', 'capital', 'town', 'township', 'reservation']):
                    index = i
                    break
            else:
                print('SKIPPED', state, name)
                continue
            # city_or_town = paragraphs[index].strip() #'City' if 'city' in chunks[1].strip().lower() else 'Town' if 'town' in chunks[1].strip().lower() else ''

            no_county = False
            for i in range(index, 5 if len(paragraphs) > 5 else len(paragraphs)):
                if any(word in paragraphs[i].strip().lower() for word in ['county', 'counties', 'seat']):
                    for chunk in paragraphs[i].split('.'):
                        if any(word in chunk.lower() for word in ['county', 'counties', 'seat']):
                            county = chunk.strip()
                            index = i
                            break
                    else:
                        print('wait, what? no state location?', 'counties')
                        continue
                    break
            else:
                for i in range(index, 5 if len(paragraphs) > 5 else len(paragraphs)):
                    if 'port' in paragraphs[i].strip().lower():
                        for chunk in paragraphs[i].split('.'):
                            if any(word in chunk.lower() for word in ['port']):
                                county = chunk.strip()
                                index = i
                                break
                        else:
                            print('wait, what? no state location?', 'port')
                            continue
                        break

                print('ALMOST COUNTY SKIPPED', state, name, city_or_town)
                county = ''
                # continue

            if county is not '':
                for chunk in county.split(' of '):
                    if any(word in chunk for word in ['county', 'counties']):
                        county = chunk
                        break
            # print(state)
            for i in range(index, len(paragraphs)):
                if any(word in paragraphs[i].strip().lower() for word in ['state', 'north', 'east', 'west', 'south', 'centr', 'adjacent']):

                    for chunk in paragraphs[i].split('.'):
                        if any(word in chunk.lower() for word in ['state', 'north', 'east', 'west', 'south', 'centr']):
                            location_state = chunk.strip()
                            location_state = getallloc(location_state, ['state', 'north', 'east', 'west', 'south', 'centr', 'adjacent'])
                            index = i
                            break
                    else:
                        print('wait, what? no state location?', 'loc ')
                        continue
                    break
            else:
                for i in range(index, len(paragraphs)):
                    if any(word in paragraphs[i].strip().lower() for word in ['city', state, ' lies ']):

                        for chunk in paragraphs[i].split('.'):
                            if any(word in chunk.lower() for word in ['city', state, ' lies ']):
                                location_state = chunk.strip()
                                location_state = getloc('[', location_state, ['city', state, ' lies '])
                                location_state = getloc(']', location_state, ['city', state, ' lies '])
                                location_state = getloc('(', location_state, ['city', state, ' lies '])
                                location_state = getloc(')', location_state, ['city', state, ' lies '])
                                location_state = getloc(';', location_state, ['city', state, ' lies '])
                                index = i
                                break
                        else:
                            print('wait, what? no state location?', 'loc city lies')
                            continue
                        break
                else:
                    for i in range(index, len(paragraphs)):
                        if any(word in paragraphs[i].strip().lower() for word in [' in ', ' is ']):

                            for chunk in paragraphs[i].split('.'):
                                if any(word in chunk.lower() for word in [' in ', ' is ']):
                                    location_state = chunk.strip()
                                    location_state = getloc('[', location_state, [' in ', ' is '])
                                    location_state = getloc(']', location_state, [' in ', ' is '])
                                    location_state = getloc('(', location_state, [' in ', ' is '])
                                    location_state = getloc(')', location_state, [' in ', ' is '])
                                    location_state = getloc(';', location_state, [' in ', ' is '])
                                    index = i
                                    break
                            else:
                                print('wait, what? no state location?', 'loc in is')
                                continue
                            break
                    else:
                        print('SKIPPED', state, name, city_or_town, county)
                        continue


            # location_state = paragraphs[index].split('.')[0].strip()
            try:
                output.write(state + '"' + name + '"' + city_or_town + '"' + county + '"' + location_state + '"' + " ".join(paragraph.split()) + '\n')
            except:
                output.write(state + '"' + name + '"' + city_or_town + '"' + county + '"' + location_state + '"' + '\n')
            # print(paragraphs)
            print('Written.')
        except:
            print('ERROR NIGGAH', state, name)
            continue

