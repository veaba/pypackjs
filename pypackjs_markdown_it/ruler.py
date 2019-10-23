from common.utils import throwError


class Ruler:
    def __init__(self):
        self.__rules = []
        self.__cache = []

    # Find rule index by name
    def __find(self, name):
        for i in range(len(self.__rules)):
            if self.__rules[i]['name'] == name:
                return i
        return -1

    # Build rules lookup cache
    def __compile(self):
        chains = ['']
        for rule in self.__rules:
            if not rule['enabled']:
                return
            for altName in rule['alt']:
                if chains.index(altName) < 0:
                    chains.append(altName)

        self.__cache = {}
        for chain in chains:
            self.__cache[chain] = []
            for rule in self.__rules:
                if not rule['enabled']:
                    return
                if chain and rule['alt'].index(chain) < 0:
                    return
                self.__cache[chain].append(rule['fn'])

    #  Replace existing typographer replacement rule with new one:
    def at(self, name, fn, options):
        index = self.__find(name)
        opt = options or {}
        if index == -1:
            return throwError('Parser rule not found:' + name)
        self.__rules[index]['fn'] = fn
        self.__rules[index]['alt'] = opt['alt'] or []
        self.__cache = None

    # Add new rule to chain before one with given name. See also
    # [[Ruler.after]], [[Ruler.push]].
    def before(self, beforeName, ruleName, fn, options):
        index = self.__find(beforeName)
        opt = options or {}
        if index == -1:
            return throwError('Parser rule not found: ' + beforeName)
        self.__rules.insert(index, {
            'name': ruleName,
            'enabled': True,
            'fn': fn,
            'alt': opt['alt'] or []
        })
        self.__cache = None

    def after(self, afterName, ruleName, fn, options):
        index = self.__find(afterName)
        opt = options or {}
        if index == -1:
            return throwError('Parser rule not found: ' + afterName)
        self.__rules.insert(index + 1, {
            'name': ruleName,
            'enabled': True,
            'fn': fn,
            'alt': opt['alt'] or []
        })
        self.__cache = None

    def push(self, ruleName, fn, options):
        opt = options or {}
        self.__rules.append({
            'name': ruleName,
            'enabled': True,
            'fn': fn,
            'alt': opt['alt'] or []
        })
        self.__cache = None

    def enable(self, array, ignoreInvalid):
        if not isinstance(array, list):
            array = [array]
        result = []
        # Search by name and enable
        for name in array:
            idx = self.__find(name)
            if idx < 0:
                if ignoreInvalid:
                    return
                return throwError('Rules manager: invalid rule name ' + name)
            self.__rules[idx]['enabled'] = True
            result.append(name)

        self.__cache = None
        return result

    # Enable rules with given names, and disable everything else. If any rule name
    # not found - throw Error. Errors can be disabled by second param.
    def enableOnly(self, array, ignoreInvalid):
        if not isinstance(array, list):
            array = [array]
        for rule in self.__rules:
            rule['enabled'] = False
        self.enable(array, ignoreInvalid)

    # Disable rules with given names. If any rule name not found - throw Error.
    # Errors can be disabled by second param.

    def disable(self, array, ignoreInvalid=None):
        if not isinstance(array, list):
            array = [array]
        result = []
        for name in array:
            idx = self.__find(name)
            if idx < 0:
                if ignoreInvalid:
                    return
                return throwError('Rules manager: invalid rule name ' + name)
            self.__rules[idx]['enabled'] = False
            result.append(name)

        self.__cache = None
        return result

    # Return array of active functions (rules) for given chain name. It analyzes
    # rules configuration, compiles caches if not exists and returns result.
    def getRules(self, chainName):
        if self.__cache is None:
            self.__compile()
        return self.__cache[chainName] or []
