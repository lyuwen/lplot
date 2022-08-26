from setuptools import setup

# Using the versioneer to set the version of the distribution
import versioneer


if __name__ == '__main__':
  name = 'lplot'
  setup(name=name,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='This is the {} module.'.format(name),
    author='Lyuwen Fu',
    #  packages=packages,
    requires=['numpy', 'PyYAML', 'matplotlib'],
    provides=['lplot'],
    #  scripts=scripts,
    include_package_data=True,
    #  test_suite='nose.collector',
    #  tests_require=['nose']
    )
