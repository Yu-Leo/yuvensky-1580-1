class Course:
    """Struct of course for page with courses list"""

    def __init__(self, link: str, logo_file_name: str, name: str, price: int, description: str):
        self.link = link  # Name of .html course's page
        self.logo_file_name = logo_file_name  # Name of file with course's logotype
        self.name = name
        self.price = price
        self.description = description
