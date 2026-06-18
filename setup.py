'''
The setup.py file is an essential part of packaging and 
distributing python projects. It is used by setuptools
(or distutils in older python versions) to define the 
configuration of your project, such as its metadata,
dependencies and more.
'''

# 
from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    '''
    This function will return list of requirements
    '''
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            # Read lines form the file 
            lines=file.readlines()
            #Process each line
            for line in lines:
                requirement=line.strip()
                #Ignore empty lines and -e .
                if requirement and requirement!= '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("Requirements.txt file not found")

    return requirement_lst


# Setting up the meta data of the of the project
setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Ayush Kashyap",
    author_email="ayush123@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)