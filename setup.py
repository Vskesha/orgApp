from setuptools import setup, find_namespace_packages

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
    packages=find_namespace_packages(),
    package_data={
        "orgapp": ["*.md", "*.txt", "*.rst", "*.png"],
        "orgapp.address_book": ["*.md", "*.txt", "*.rst", "*.png"],
        "orgapp.bandergoose": ["*.md", "*.txt", "*.rst", "*.png"],
        "orgapp.hannoitower": ["*.md", "*.txt", "*.rst", "*.png"],
        "orgapp.note_book": ["*.md", "*.txt", "*.rst", "*.png"],
        "orgapp.snake": ["*.md", "*.txt", "*.rst", "*.png"],
        "orgapp.sorter": ["*.md", "*.txt", "*.rst", "*.png"],
        "orgapp.tictactoe": ["*.md", "*.txt", "*.rst", "*.png"],
    },
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
            "orgapp = main:main"
            "addressbook = address_book.address_book:main"
            "notebook = note_book.note_book:main"
            "sorter = sorter.sorter:clean_folder"
        ],
        'gui-scripts': [
            "bandergoose = bandergoose.bandergoose:main"
            "hannoitower = hannoitower.hannoitower:main"
            "snake = snake.snake:main"
            "tictactoe = tictactoe.tictactoe:main"
        ]
    }
)