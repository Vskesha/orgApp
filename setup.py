from setuptools import setup
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
long_description += (this_directory / 'orgapp' / 'address_book' / 'README.md').read_text()
long_description += (this_directory / 'orgapp' / 'note_book' / 'README.md').read_text()
long_description += (this_directory / 'orgapp' / 'sorter' / 'README.md').read_text()


setup(
    name="orgApp",
    version='0.0.3',
    description="personal organizing tool",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/Vskesha/orgApp",
    author='Vasyl Boliukh, '
           'Olga Sirenko, '
           'Oleh Kolobaiev, '
           'Andriy Batig',
    author_email='vskesha@gmail.com, '
                 'olga19022020@gmail.com, '
                 'o.kolobaiev@gmail.com, '
                 'ashabatig1992@gmail.com',
    license='MIT License',
    packages=[
        "orgapp",
        "orgapp.address_book",
        "orgapp.bandergoose",
        "orgapp.hannoitower",
        "orgapp.note_book",
        "orgapp.snake",
        "orgapp.sorter",
        "orgapp.tictactoe"
    ],
    include_package_data=True,
    install_requires=[
        'markdown',
        "colorama==0.4.6",
        "prompt-toolkit==3.0.39",
        "pygame==2.5.1",
        "wcwidth==0.2.6",
        'Faker==19.6.1'
    ],
    entry_points={
        'console_scripts': [
            "orgapp = orgapp.main:main",
            "abk = orgapp.address_book.address_book:main",
            "addressbook = orgapp.address_book.address_book:main",
            "nbk = orgapp.note_book.note_book:main",
            "notebook = orgapp.note_book.note_book:main",
            "sorter = orgapp.sorter.sorter:clean_folder",
        ],
        'gui_scripts': [
            "bandergoose = orgapp.bandergoose.bandergoose:main",
            "hannoitower = orgapp.hannoitower.hannoitower:main",
            "snake = orgapp.snake.snake:main",
            "tictactoe = orgapp.tictactoe.tictactoe:main"
        ]
    }
)
