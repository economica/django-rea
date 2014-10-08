from setuptools import setup, find_packages

setup( name='django-rea',
    version = '0.0.1',
    description = 'Resources, Events & Agents marketplace models',
    author = 'Daryl Antony',
    author_email = 'daryl@economica.io',
    url = 'https://github.com/economica/rea',
    keywords = ['django',],
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires = [
        'Django>=1.7',
        'django-polymorphic',
        'django-xworkflows',
        'django-uuidfield',
    ]
)
