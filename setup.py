from setuptools import setup

setup(
    name="orgApp",
    version='0.0.1',
    description="personal organizing tool",
    url="https://github.com/Vskesha/orgApp",
    author='Vasyl Boliukh, '
           'Olga Sirenko, '
           'Oleh Kolobaiev, '
           'Andriy Batig, '
           'Nataliya Schvab',
    author_email='vskesha@gmail.com, '
                 'olga19022020@gmail.com, '
                 'o.kolobaiev@gmail.com, '
                 'ashabatig1992@gmail.com, '
                 'shnataliya77@gmail.com',
    license='MIT',
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
        "wcwidth==0.2.6"
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
