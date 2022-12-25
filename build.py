import os
from os import path
from pathlib import Path
from io import BytesIO
from lxml import etree


SONG_BOOKS_DIR = './songbooks'

class Song:
    def __init__(self, name, category, content, name2=None, tags=''):
        self.name = name
        self.name2 = name2 or name
        self.font = 'TAU_Elango_Ragham'
        self.font2 = 'Verdana'
        self.copyright = 'FGPC'
        self.notes = ''
        self.key = ''
        self.bkgnd = 'null'
        self.yvideo = ''
        self.timestamp = '11/4/2022  9:4'
        self.category = category
        self.tags = tags
        self.slide = self.parse_slides(content)
        self.slide2 = ''
        self.slideseq = ''

    @staticmethod
    def parse_slides(content):
        data = []
        slides = content.split(os.linesep * 2)
        for sln in slides:
            sln = sln.strip().replace(os.linesep, '<br>') + '<slide>'
            data.append(sln)
        return ''.join(data)

    def to_xml(self):
        song = etree.Element('song')

        category = etree.Element('category')
        category.text = self.category
        song.append(category)

        name = etree.Element('name')
        name.text = self.name
        song.append(name)

        name2 = etree.Element('name2')
        name2.text = etree.CDATA(self.name2)
        song.append(name2)

        font = etree.Element('font')
        font.text = self.font
        song.append(font)

        font2 = etree.Element('font2')
        font2.text = self.font2
        song.append(font2)

        timestamp = etree.Element('timestamp')
        timestamp.text = self.timestamp
        song.append(timestamp)

        yvideo = etree.Element('yvideo')
        yvideo.text = self.yvideo
        song.append(yvideo)

        bkgnd = etree.Element('bkgnd')
        bkgnd.text = self.bkgnd
        song.append(bkgnd)

        key = etree.Element('key')
        key.text = self.key
        song.append(key)

        copyright = etree.Element('copyright')
        copyright.text = self.copyright
        song.append(copyright)

        notes = etree.Element('notes')
        notes.text = self.notes
        song.append(notes)

        slide = etree.Element('slide')
        slide.text = etree.CDATA(self.slide)
        song.append(slide)

        slide2 = etree.Element('slide2')
        slide2.text = etree.CDATA(self.slide2)
        song.append(slide2)

        tags = etree.Element('tags')
        tags.text = etree.CDATA(self.tags)
        song.append(tags)

        slideseq = etree.Element('slideseq')
        slideseq.text = etree.CDATA(self.slideseq)
        song.append(slideseq)

        return song


def parse_song(filename: str) -> Song:
    song_name, _ = path.splitext(filename)
    _, category, song_name = song_name.replace('\\', '/').split('/')

    with open(filename, 'rb') as sc:
        content = sc.read().decode('utf-8')

    return Song(song_name, category, content)
    

def load_songs():
    songs = []

    files = Path(SONG_BOOKS_DIR).glob('*/*.song')
    for file in files:
        print(f'Compiling Song: {file}')
        songs.append(parse_song(file))

    return songs

def main():
    songDB = etree.Element('songDB')

    _type = etree.Element('type')
    _type.text = 'XMLsong'
    songDB.append(_type)

    disclaimer = etree.Element('disclaimer')
    disclaimer.text = 'The copyrights to these songs belongs to person mentioned in the copyright tag of each song. This database has been designed and compiled for VerseVIEW only.'
    songDB.append(disclaimer)

    songs = load_songs()
    for song in songs:
        songDB.append(song.to_xml())

    fp = BytesIO()
    songDB.getroottree().write(
        fp, 
        pretty_print=True, 
        encoding='utf-8',
        xml_declaration=True,
    )

    with open('./dist/vv_songs.xml', 'wb') as df:
        df.write(fp.getvalue())

if __name__ == '__main__':
    main()
