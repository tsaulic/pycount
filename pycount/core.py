# -*- coding: utf-8 -*-
# pylint: disable=R0912


"""
   pycount.pycount
   ~~~~~~~~~~~~~~~

   Core pycount file

   :copyright: (c) Tihomir Saulic
   :license: DO WHAT YOU WANT TO PUBLIC LICENSE, see LICENSE for more details
"""


from __future__ import print_function

import hashlib
import os
import pkg_resources
import re
import sys
import time

try:
    from binaryornot.check import is_binary
except ImportError as an_error:
    sys.exit(an_error)


VERSION = pkg_resources.require("pycount")[0].version

def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes
    """
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk


def timer(method):
    """Measures a method running time
    """
    def timed(self):
        """New decorated function
        """
        start = time.time()
        method(self)
        end = time.time()
        runtime = end - start
        self.times.append(runtime)
    return timed


def exact_match(phrase, word):
    b = r'(\s|^|$)' 
    res = re.match(b + word + b, phrase, flags=re.IGNORECASE)
    return bool(res)


def isfile(obj):
    """Check whether a file or not
    """
    if type(obj) is str and os.path.isfile(obj):
        return True


class NoPathException(Exception):
    """Exception for when a path is not given, but is necessary to be passed as
       an argument
    """
    pass


class Counter(object):
    """Main clas for counting the lines of code
    """
    def __init__(self, root=None, patterns=None, by_files=None):
        if root is None:
            self.root = os.getcwd()
        else:
            self.root = root

        self.files = None
        self.hashes = None
        self.results = None
        self.times = []

        if patterns is None:
            self.patterns = {
                '.abap': 'ABAP',
                '.ac': 'm4',
                '.ada': 'Ada',
                '.adb': 'Ada',
                '.ads': 'Ada',
                '.adso': 'ADSO/IDSM',
                '.ahk': 'AutoHotkey',
                '.am': 'make',
                '.ample': 'AMPLE',
                '.as': 'ActionScript',
                '.dofile': 'AMPLE',
                '.startup': 'AMPLE',
                '.asa': 'ASP',
                '.asax': 'ASP.Net',
                '.ascx': 'ASP.Net',
                '.asm': 'Assembly',
                '.asmx': 'ASP.Net',
                '.asp': 'ASP',
                '.aspx': 'ASP.Net',
                '.master': 'ASP.Net',
                '.sitemap': 'ASP.Net',
                '.cshtml': 'Razor',
                '.bas': 'Visual Basic',
                '.bat': 'DOS Batch',
                '.BAT': 'DOS Batch',
                '.build.xml': 'Ant',
                '.cbl': 'COBOL',
                '.CBL': 'COBOL',
                '.c': 'C',
                '.C': 'C++',
                '.cc': 'C++',
                '.c++': 'C++',
                '.ccs': 'CCS',
                '.cfc': 'ColdFusion CFScript',
                '.cfm': 'ColdFusion',
                '.cl': 'Lisp/OpenCL',
                '.clj': 'Clojure',
                '.cljs': 'ClojureScript',
                '.cls': 'Visual Basic',
                '.CMakeLists.txt': 'CMake',
                '.cmake': 'CMake',
                '.cob': 'COBOL',
                '.COB': 'COBOL',
                '.coffee': 'CoffeeScript',
                '.component': 'Visualforce Component',
                '.config': 'ASP.Net',
                '.cpp': 'C++',
                '.cs': 'C#',
                '.css': "CSS",
                '.ctl': 'Visual Basic',
                '.cxx': 'C++',
                '.d': 'D',
                '.da': 'DAL',
                '.dart': 'Dart',
                '.def': 'Teamcenter def',
                '.dmap': 'NASTRAN DMAP',
                '.dpr': 'Pascal',
                '.dsr': 'Visual Basic',
                '.dtd': 'DTD',
                '.ec': 'C',
                '.el': 'Lisp',
                '.erl': 'Erlang',
                '.exp': 'Expect',
                '.f77': 'Fortran 77',
                '.F77': 'Fortran 77',
                '.f90': 'Fortran 90',
                '.F90': 'Fortran 90',
                '.f95': 'Fortran 95',
                '.F95': 'Fortran 95',
                '.f': 'Fortran 77',
                '.F': 'Fortran 77',
                '.fmt': 'Oracle Forms',
                '.focexec': 'Focus',
                '.frm': 'Visual Basic',
                '.gnumakefile': 'make',
                '.Gnumakefile': 'make',
                '.go': 'Go',
                '.groovy': 'Groovy',
                '.gant': 'Groovy',
                '.h': 'C/C++ Header',
                '.H': 'C/C++ Header',
                '.hh': 'C/C++ Header',
                '.hpp': 'C/C++ Header',
                '.hrl': 'Erlang',
                '.hs': 'Haskell',
                '.htm': 'HTML',
                '.html': 'HTML',
                '.i3': 'Modula3',
                '.ism': 'InstallShield',
                '.pro': 'IDL',
                '.ig': 'Modula3',
                '.il': 'SKILL',
                '.ils': 'SKILL++',
                '.inc': 'PHP/Pascal',
                '.ino': 'Arduino Sketch',
                '.pde': 'Arduino Sketch',
                '.itk': 'Tcl/Tk',
                '.java': 'Java',
                '.jcl': 'JCL',
                '.jl': 'Lisp',
                '.js': 'Javascript',
                '.jsf': 'JavaServer Faces',
                '.json': 'JSON',
                '.xhtml': 'JavaServer Faces',
                '.jsp': 'JSP',
                '.ksc': 'Kermit',
                '.lhs': 'Haskell',
                '.l': 'lex',
                '.less': 'LESS',
                '.lsp': 'Lisp',
                '.lisp': 'Lisp',
                '.m3': 'Modula3',
                '.m4': 'm4',
                '.makefile': 'make',
                '.Makefile': 'make',
                '.met': 'Teamcenter met',
                '.wdproj': 'MSBuild script',
                '.vcproj': 'MSBuild script',
                '.wixproj': 'MSBuild script',
                '.vbproj': 'MSBuild script',
                '.csproj': 'MSBuild script',
                '.mg': 'Modula3',
                '.ml': 'OCaml',
                '.mli': 'OCaml',
                '.mly': 'OCaml',
                '.mll': 'OCaml',
                '.m': 'MATLAB/Objective C/MUMPS',
                '.mm': 'Objective C++',
                '.wdproj': 'MSBuild scripts',
                '.csproj': 'MSBuild scripts',
                '.mps': 'MUMPS',
                '.mth': 'Teamcenter mth',
                '.oscript': 'LiveLink OScript',
                '.pad': 'Ada',
                '.page': 'Visualforce Page',
                '.pas': 'Pascal',
                '.pcc': 'C++',
                '.pfo': 'Fortran 77',
                '.pgc': 'C',
                '.php3': 'PHP',
                '.php4': 'PHP',
                '.php5': 'PHP',
                '.php': 'PHP',
                '.pig': 'Pig Latin',
                '.plh': 'Perl',
                '.pl': 'Perl',
                '.PL': 'Perl',
                '.plx': 'Perl',
                '.pm': 'Perl',
                '.pom.xml': 'Maven',
                '.pom': 'Maven',
                '.p': 'Pascal',
                '.pp': 'Pascal',
                '.psql': 'SQL',
                '.py': 'Python',
                '.pyx': 'Cython',
                '.qml': 'QML',
                '.rb': 'Ruby',
                '.rex': 'Oracle Reports',
                '.rexx': 'Rexx',
                '.rhtml': 'Ruby HTML',
                '.rs': 'Rust',
                '.s': 'Assembly',
                '.S': 'Assembly',
                '.scala': 'Scala',
                '.sbl': 'Softbridge Basic',
                '.SBL': 'Softbridge Basic',
                '.sc': 'Lisp',
                '.scm': 'Lisp',
                '.ses': 'Patran Command Language',
                '.pcl': 'Patran Command Language',
                '.ps1': 'PowerShell',
                '.sass': 'SASS',
                '.scss': 'SASS',
                '.smarty': 'Smarty',
                '.sql': 'SQL',
                '.SQL': 'SQL',
                '.sproc.sql': 'SQL Stored Procedure',
                '.spoc.sql': 'SQL Stored Procedure',
                '.spc.sql': 'SQL Stored Procedure',
                '.udf.sql': 'SQL Stored Procedure',
                '.data.sql': 'SQL Data',
                '.v': 'Verilog-SystemVerilog',
                '.sv': 'Verilog-SystemVerilog',
                '.svh': 'Verilog-SystemVerilog',
                '.tk': 'Tcl/Tk',
                '.tpl': 'Smarty',
                '.trigger': 'Apex Trigger',
                '.vala': 'Vala',
                '.vapi': 'Vala Header',
                '.vhd': 'VHDL',
                '.VHD': 'VHDL',
                '.vhdl': 'VHDL',
                '.VHDL': 'VHDL',
                '.vba': 'Visual Basic',
                '.VBA': 'Visual Basic',
                '.vb': 'Visual Basic',
                '.VB': 'Visual Basic',
                '.vbs': 'Visual Basic',
                '.VBS': 'Visual Basic',
                '.webinfo': 'ASP.Net',
                '.xml': 'XML',
                '.XML': 'XML',
                '.mxml': 'MXML',
                '.build': 'NAnt scripts',
                '.vim': 'vim script',
                '.xaml': 'XAML',
                '.xsd': 'XSD',
                '.XSD': 'XSD',
                '.xslt': 'XSLT',
                '.XSLT': 'XSLT',
                '.xsl': 'XSLT',
                '.XSL': 'XSLT',
                '.y': 'yacc',
                '.yaml': 'YAML',
                '.yml': 'YAML',
                '.awk': 'awk',
                '.bash': 'Bourne Again Shell',
                '.bc': 'bc',
                '.csh': 'C Shell',
                '.dmd': 'D',
                '.idl': 'IDL',
                '.kermit': 'Kermit',
                '.ksh': 'Korn Shell',
                '.lua': 'Lua',
                '.make': 'make',
                '.octave': 'Octave',
                '.perl5': 'Perl',
                '.perl': 'Perl',
                '.ruby': 'Ruby',
                '.sed': 'sed',
                '.sh': 'Bourne Shell',
                '.tcl': 'Tcl/Tk',
                '.tclsh': 'Tcl/Tk',
                '.tcsh': 'C Shell',
                '.wish': 'Tcl/Tk'
            }
        else:
            self.patterns = patterns

        if by_files is None:
            self.by_files = {
                'Makefile': 'make',
                'makefile': 'make',
                'gnumakefile': 'make',
                'Gnumakefile': 'make',
                'CMakeLists.txt': 'CMake',
                'build.xml': 'Ant/XML',
                'pom.xml': 'Maven/XML',
                'Rakefile': 'Ruby',
                'rakefile': 'Ruby'
            }
        else:
            self.by_files = by_files

        self.ignore = ['.git', '.hg', '.svn']

    def unique(self, a_file, hashing=hashlib.sha1, unique=False):
        """Filters out duplicate files
        """
        hashobj = hashing()
        for chunk in chunk_reader(open(a_file, "rb")):
            hashobj.update(chunk)
        file_id = (hashobj.digest(), os.path.getsize(a_file))
        duplicate = self.hashes.get(file_id, None)
        if duplicate:
            pass
        else:
            self.hashes[file_id] = a_file
            unique = True
        return unique

    def walker(self, fpath=None, a_file=None):
        """Takes care of finding actual files that need to be added to the
           self.files
        """
        import pdb
        if a_file is not None:
            try:
                has_data = os.stat(a_file).st_size > 0
            except OSError:
                has_data = False
            if has_data and self.unique(a_file) and not is_binary(a_file) \
                    and not os.path.islink(a_file):
                self.files.append(a_file)
        if fpath is not None:
            for path, subpaths, files in os.walk(fpath):
                for pattern in self.ignore:
                    if pattern in subpaths:
                        subpaths.remove(pattern)
                for a_file in files:
                    for entry in self.by_files.keys():
                        try:
                            has_data = os.stat(a_file).st_size > 0
                        except OSError:
                            has_data = False
                        if exact_match(a_file, entry) and has_data and \
                                self.unique(a_file) and not \
                                is_binary(a_file) and not \
                                os.path.islink(a_file):
                            single_file = os.path.join(path, a_file)
                            self.files.append(single_file)
                    if not a_file.startswith("."):
                        a_file = os.path.join(path, a_file)
                        try:
                            has_data = os.stat(a_file).st_size > 0
                        except OSError:
                            has_data = False
                        if has_data and self.unique(a_file) and not \
                                is_binary(a_file) and not \
                                os.path.islink(a_file):
                            self.files.append(a_file)
                            if len(self.files) < 100 and len(self.files) \
                                    % 10 == 0:
                                sys.stdout.write("\r%d unique files"
                                                 % len(self.files))
                                sys.stdout.flush()
                            elif self.files and len(self.files) % 100 == 0:
                                sys.stdout.write("\r%d unique files"
                                                 % len(self.files))
                                sys.stdout.flush()
            print("", end="\r")
        if (fpath and a_file) is None:
            raise NoPathException("Method needs a path to work.")

    @timer
    def discover(self):
        """Used to determine what type of dataset user has provided and act
           based on that information. It calls walker() to do actual file
           discovery
        """
        self.files = []
        self.hashes = {}

        if type(self.root) is str and os.path.isfile(self.root):
            self.walker(a_file=self.root)
        elif type(self.root) is str:
            if os.path.exists(self.root):
                self.walker(fpath=self.root)
            else:
                print("Invalid path specified: %s" % self.root)
        elif type(self.root) is list:
            for fpath in self.root:
                if isfile(fpath):
                    self.walker(a_file=fpath)
                if os.path.exists(fpath):
                    self.walker(fpath=fpath)
                else:
                    print("Invalid path specified: %s" % fpath)
        self.total_uniques = len(self.files)
        print(str(self.total_uniques) + " unique files")

    @timer
    def count(self):
        """Counts lines of code for valid files in self.patterns
        """
        self.results = {}
        self.file_types = {}

        for fpath in self.files:
            fname = os.path.splitext(os.path.basename(fpath))[0]
            ext = os.path.splitext(fpath)[1]
            count = 0
            file_type_count = 0
            if fname in self.by_files.keys():
                with open(fpath, "r") as a_file:
                    for line in a_file:
                        if line.strip():
                            count += 1
                file_type_count += 1
                try:
                    self.file_types[self.by_files[fname]] += file_type_count
                except KeyError:
                    self.file_types[self.by_files[fname]] = 0
                    self.file_types[self.by_files[fname]] += file_type_count
                try:
                    self.results[self.by_files[fname]] += count
                except KeyError:
                    self.results[self.by_files[fname]] = 0
                    self.results[self.by_files[fname]] += count
            if ext in self.patterns.keys():
                with open(fpath, "r") as a_file:
                    for line in a_file:
                        if line.strip():
                            count += 1
                file_type_count += 1
                try:
                    self.file_types[self.patterns[ext]] += file_type_count
                except KeyError:
                    self.file_types[self.patterns[ext]] = 0
                    self.file_types[self.patterns[ext]] += file_type_count
                try:
                    self.results[self.patterns[ext]] += count
                except KeyError:
                    self.results[self.patterns[ext]] = 0
                    self.results[self.patterns[ext]] += count

    @timer
    def report(self):
        """Generates and prints a decent looking breakdown report for lines
           of code for all existent languages under our path
        """
        if self.results:
            counted = sum(self.file_types.values())
            print(str((self.total_uniques - counted)) + " ignored files.")
            print("ver: " + VERSION)
            print("\nLanguage                       Files         LOC")
            print("-" * 48)
            for key, value in sorted(self.results.items(), key=lambda x: x[1],
                                     reverse=True):
                if value is not 0:
                    print("{0:24}     {1:7d}     {2:7d}".format(key, self.file_types[key], value))
            print("-" * 48)
            print("{0:24}     {1:7d}   {2:9d}".format("SUM:", counted,
                  sum(self.results.values())))
            print("-" * 48)
            print("{0:24} {1:23.2f}".format("RUNTIME (sec):", sum(self.times)))
            print("-" * 48)
        else:
            print("No results.")
