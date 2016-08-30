from calmjs import bower

if __name__ == '__main__':
    # XXX workaround the nonsensical default prog assignment.
    bower.bower.runtime.argparser.prog = 'bower'
    bower.bower.runtime()
