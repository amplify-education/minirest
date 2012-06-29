from distutils.core import setup
setup(name = 'MiniREST',
      version = '1.0',
      description = 'MiniREST http server/client + daemon',
      # Required packages
      requires = [ 'simplejson', 'gevent'],
      # List what we provide and obolete for updates
      provides = ['MiniREST', 'daemon'],
      obsoletes = ['MiniREST', 'daemon'],
      # Seperate modules
      py_modules = [
          'daemon', 
          ],
      # Main packages
      packages = ['MiniREST'],
      )
