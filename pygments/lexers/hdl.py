"""
    pygments.lexers.hdl
    ~~~~~~~~~~~~~~~~~~~

    Lexers for hardware descriptor languages.

    :copyright: Copyright 2006-2021 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import RegexLexer, bygroups, include, using, this, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation

from pygments.lexers import _systemverilog_builtins

__all__ = ['VerilogLexer', 'SystemVerilogLexer', 'VhdlLexer']


class VerilogLexer(RegexLexer):
    """
    For verilog source code with preprocessor directives.

    .. versionadded:: 1.4
    """
    name = 'verilog'
    aliases = ['verilog', 'v']
    filenames = ['*.v']
    mimetypes = ['text/x-verilog']

    #: optional Comment or Whitespace
    _ws = r'(?:\s|//.*?\n|/[*].*?[*]/)+'

    tokens = {
        'root': [
            (r'^\s*`define', Comment.Preproc, 'macro'),
            (r'\n', Text),
            (r'\s+', Text),
            (r'\\\n', Text),  # line continuation
            (r'/(\\\n)?/(\n|(.|\n)*?[^\\]\n)', Comment.Single),
            (r'/(\\\n)?[*](.|\n)*?[*](\\\n)?/', Comment.Multiline),
            (r'[{}#@]', Punctuation),
            (r'L?"', String, 'string'),
            (r"L?'(\\.|\\[0-7]{1,3}|\\x[a-fA-F0-9]{1,2}|[^\\\'\n])'", String.Char),
            (r'(\d+\.\d*|\.\d+|\d+)[eE][+-]?\d+[lL]?', Number.Float),
            (r'(\d+\.\d*|\.\d+|\d+[fF])[fF]?', Number.Float),
            (r'([0-9]+)|(\'h)[0-9a-fA-F]+', Number.Hex),
            (r'([0-9]+)|(\'b)[01]+', Number.Bin),
            (r'([0-9]+)|(\'d)[0-9]+', Number.Integer),
            (r'([0-9]+)|(\'o)[0-7]+', Number.Oct),
            (r'\'[01xz]', Number),
            (r'\d+[Ll]?', Number.Integer),
            (r'[~!%^&*+=|?:<>/-]', Operator),
            (r'[()\[\],.;\']', Punctuation),
            (r'`[a-zA-Z_]\w*', Name.Constant),

            (r'^(\s*)(package)(\s+)', bygroups(Text, Keyword.Namespace, Text)),
            (r'^(\s*)(import)(\s+)', bygroups(Text, Keyword.Namespace, Text),
             'import'),

            (words((
                'always', 'always_comb', 'always_ff', 'always_latch', 'and',
                'assign', 'automatic', 'begin', 'break', 'buf', 'bufif0', 'bufif1',
                'case', 'casex', 'casez', 'cmos', 'const', 'continue', 'deassign',
                'default', 'defparam', 'disable', 'do', 'edge', 'else', 'end', 'endcase',
                'endfunction', 'endgenerate', 'endmodule', 'endpackage', 'endprimitive',
                'endspecify', 'endtable', 'endtask', 'enum', 'event', 'final', 'for',
                'force', 'forever', 'fork', 'function', 'generate', 'genvar', 'highz0',
                'highz1', 'if', 'initial', 'inout', 'input', 'integer', 'join', 'large',
                'localparam', 'macromodule', 'medium', 'module', 'nand', 'negedge',
                'nmos', 'nor', 'not', 'notif0', 'notif1', 'or', 'output', 'packed',
                'parameter', 'pmos', 'posedge', 'primitive', 'pull0', 'pull1',
                'pulldown', 'pullup', 'rcmos', 'ref', 'release', 'repeat', 'return',
                'rnmos', 'rpmos', 'rtran', 'rtranif0', 'rtranif1', 'scalared', 'signed',
                'small', 'specify', 'specparam', 'strength', 'string', 'strong0',
                'strong1', 'struct', 'table', 'task', 'tran', 'tranif0', 'tranif1',
                'type', 'typedef', 'unsigned', 'var', 'vectored', 'void', 'wait',
                'weak0', 'weak1', 'while', 'xnor', 'xor'), suffix=r'\b'),
             Keyword),

            (words((
                'accelerate', 'autoexpand_vectornets', 'celldefine', 'default_nettype',
                'else', 'elsif', 'endcelldefine', 'endif', 'endprotect', 'endprotected',
                'expand_vectornets', 'ifdef', 'ifndef', 'include', 'noaccelerate',
                'noexpand_vectornets', 'noremove_gatenames', 'noremove_netnames',
                'nounconnected_drive', 'protect', 'protected', 'remove_gatenames',
                'remove_netnames', 'resetall', 'timescale', 'unconnected_drive',
                'undef'), prefix=r'`', suffix=r'\b'),
             Comment.Preproc),

            (words((
                'bits', 'bitstoreal', 'bitstoshortreal', 'countdrivers', 'display', 'fclose',
                'fdisplay', 'finish', 'floor', 'fmonitor', 'fopen', 'fstrobe', 'fwrite',
                'getpattern', 'history', 'incsave', 'input', 'itor', 'key', 'list', 'log',
                'monitor', 'monitoroff', 'monitoron', 'nokey', 'nolog', 'printtimescale',
                'random', 'readmemb', 'readmemh', 'realtime', 'realtobits', 'reset',
                'reset_count', 'reset_value', 'restart', 'rtoi', 'save', 'scale', 'scope',
                'shortrealtobits', 'showscopes', 'showvariables', 'showvars', 'sreadmemb',
                'sreadmemh', 'stime', 'stop', 'strobe', 'time', 'timeformat', 'write'),
                prefix=r'\$', suffix=r'\b'),
             Name.Builtin),

            (words((
                'byte', 'shortint', 'int', 'longint', 'integer', 'time',
                'bit', 'logic', 'reg', 'supply0', 'supply1', 'tri', 'triand',
                'trior', 'tri0', 'tri1', 'trireg', 'uwire', 'wire', 'wand', 'wor'
                'shortreal', 'real', 'realtime'), suffix=r'\b'),
             Keyword.Type),
            (r'[a-zA-Z_]\w*:(?!:)', Name.Label),
            (r'\$?[a-zA-Z_]\w*', Name),
            (r'\\(\S+)', Name),
        ],
        'string': [
            (r'"', String, '#pop'),
            (r'\\([\\abfnrtv"\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
            (r'[^\\"\n]+', String),  # all other characters
            (r'\\\n', String),  # line continuation
            (r'\\', String),  # stray backslash
        ],
        'macro': [
            (r'[^/\n]+', Comment.Preproc),
            (r'/[*](.|\n)*?[*]/', Comment.Multiline),
            (r'//.*?\n', Comment.Single, '#pop'),
            (r'/', Comment.Preproc),
            (r'(?<=\\)\n', Comment.Preproc),
            (r'\n', Comment.Preproc, '#pop'),
        ],
        'import': [
            (r'[\w:]+\*?', Name.Namespace, '#pop')
        ]
    }

    def analyse_text(text):
        """Verilog code will use one of reg/wire/assign for sure, and that
        is not common elsewhere."""
        result = 0
        if 'reg' in text:
            result += 0.1
        if 'wire' in text:
            result += 0.1
        if 'assign' in text:
            result += 0.1

        return result


class SystemVerilogLexer(RegexLexer):
    """
    Extends verilog lexer to recognise all SystemVerilog keywords from IEEE
    1800-2009 standard.

    .. versionadded:: 1.5
    """
    name = 'systemverilog'
    aliases = ['systemverilog', 'sv']
    filenames = ['*.sv', '*.svh']
    mimetypes = ['text/x-systemverilog']

    #: optional Comment or Whitespace
    _ws = r'(?:\s|//.*?\n|/[*].*?[*]/)+'

    lifetime = 'static|automatic'

    tokens = {
        'root': [
            (r'^\s*`define', Comment.Preproc, 'macro'),
            (r'^(\s*)(import)(\s+)', bygroups(Text, Keyword.Namespace, Text), 'import'),
            (r'(function)(\s+)', bygroups(Keyword.Declaration, Text), 'function'),
            (r'(endfunction\b)(?:(\s*)(:)(\s*)([a-zA-Z_]\w*))?',
             bygroups(Keyword.Declaration, Text, Punctuation, Text, Name.Function)),

            (r'\n', Text),
            (r'\s+', Text),
            (r'\\\n', Text),  # line continuation
            (r'/(\\\n)?/(\n|(.|\n)*?[^\\]\n)', Comment.Single),
            (r'/(\\\n)?[*](.|\n)*?[*](\\\n)?/', Comment.Multiline),
            (r'[{}#@]', Punctuation),
            (r'L?"', String, 'string'),
            (r"L?'(\\.|\\[0-7]{1,3}|\\x[a-fA-F0-9]{1,2}|[^\\\'\n])'", String.Char),

            (r'(\d+\.\d*|\.\d+|\d+)[eE][+-]?\d+[lL]?', Number.Float),
            (r'(\d+\.\d*|\.\d+|\d+[fF])[fF]?', Number.Float),

            (r'([1-9][_0-9]*)?\s*\'[sS]?[bB]\s*[xXzZ?01][_xXzZ?01]*',
             Number.Bin),
            (r'([1-9][_0-9]*)?\s*\'[sS]?[oO]\s*[xXzZ?0-7][_xXzZ?0-7]*',
             Number.Oct),
            (r'([1-9][_0-9]*)?\s*\'[sS]?[dD]\s*[xXzZ?0-9][_xXzZ?0-9]*',
             Number.Integer),
            (r'([1-9][_0-9]*)?\s*\'[sS]?[hH]\s*[xXzZ?0-9a-fA-F][_xXzZ?0-9a-fA-F]*',
             Number.Hex),

            (r'\'[01xXzZ]', Number),
            (r'[0-9][_0-9]*', Number.Integer),

            (r'[~!%^&*+=|?:<>/-]', Operator),
            (words(('inside', 'dist'), suffix=r'\b'), Operator.Word),

            (r'[()\[\],.;\']', Punctuation),
            (r'(\$)(\s*)(\])', bygroups(Punctuation, Text, Punctuation)),
            (r'`[a-zA-Z_]\w*', Name.Constant),

            (words(_systemverilog_builtins.KEYWORDS, suffix=r'\b'), Keyword),

            # package declaration
            (r'^(\s*)(package)(\s+)([a-zA-Z_]\w*)',
             bygroups(Text, Keyword.Namespace, Text, Name.Namespace)),
            (r'(endpackage\b)(?:(\s*)(:)(\s*)([a-zA-Z_]\w*))?',
             bygroups(Keyword.Namespace, Text, Punctuation, Text, Name.Namespace)),

            # interface declaration
            (r'^(\s*)(interface)(\s+)(?!class )([a-zA-Z_]\w*)',
             bygroups(Text, Keyword.Declaration, Text, Name.Class)),
            (r'(endinterface\b)(?:(\s*)(:)(\s*)([a-zA-Z_]\w*))?',
             bygroups(Keyword.Declaration, Text, Punctuation, Text, Name.Class)),

            # module declaration
            (r'^(\s*)(module)(\s+)([a-zA-Z_]\w*)',
             bygroups(Text, Keyword.Declaration, Text, Name.Class)),
            (r'(endmodule\b)(?:(\s*)(:)(\s*)([a-zA-Z_]\w*))?',
             bygroups(Keyword.Declaration, Text, Punctuation, Text, Name.Class)),

            (r'(task)(\s+)({})(\s+)([a-zA-Z_]\w*)'.format(lifetime),
             bygroups(Keyword.Declaration, Text, Keyword, Text, Name.Function)),
            (r'(task)(\s+)([a-zA-Z_]\w*)',
             bygroups(Keyword.Declaration, Text, Name.Function)),
            (r'(endtask\b)(?:(\s*)(:)(\s*)([a-zA-Z_]\w*))?',
             bygroups(Keyword.Declaration, Text, Punctuation, Text, Name.Function)),

            # class declaration
            (r'(interface)?(\s*)(class)(\s+)([a-zA-Z_]\w*)',
             bygroups(Keyword, Text, Keyword.Declaration, Text, Name.Class)),
            (r'(extends)(\s+)([a-zA-Z_]\w*)',
             bygroups(Keyword.Declaration, Text, Name.Class)),
            (r'(endclass\b)(?:(\s*)(:)(\s*)([a-zA-Z_]\w*))?',
             bygroups(Keyword.Declaration, Text, Punctuation, Text, Name.Class)),

            (words(_systemverilog_builtins.DATA_TYPES, suffix=r'\b'), Keyword.Type),
            (words(_systemverilog_builtins.NET_TYPES, suffix=r'\b'), Keyword.Type),
            (words(_systemverilog_builtins.PREPROCS, suffix=r'\b'), Comment.Preproc),
            (words(_systemverilog_builtins.BUILTIN_FUNTIONS, suffix=r'\b'), Name.Builtin),

            (r'[a-zA-Z_]\w*:(?!:)', Name.Label),
            (r'\$?[a-zA-Z_]\w*', Name),
            (r'\\(\S+)', Name),
        ],
        'string': [
            (r'"', String, '#pop'),
            (r'\\([\\abfnrtv"\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
            (r'[^\\"\n]+', String),  # all other characters
            (r'\\\n', String),  # line continuation
            (r'\\', String),  # stray backslash
        ],
        'macro': [
            (r'[^/\n]+', Comment.Preproc),
            (r'/[*](.|\n)*?[*]/', Comment.Multiline),
            (r'//.*?\n', Comment.Single, '#pop'),
            (r'/', Comment.Preproc),
            (r'(?<=\\)\n', Comment.Preproc),
            (r'\n', Comment.Preproc, '#pop'),
        ],
        'import': [
            (r'[\w:]+\*?', Name.Namespace, '#pop')
        ],
        'function': [
            (r'\s+', Text),
            (r'(static\b|automatic\b)', Keyword),
            (words(_systemverilog_builtins.DATA_TYPES, suffix=r'\b'), Keyword.Type),
            (r'[\[\]:]', Punctuation),
            (r'[0-9]+', Number.Integer),
            (r'([a-zA-Z_]\w*)', Name.Function),
            (r'\(', Punctuation, '#pop')
        ],
    }


class VhdlLexer(RegexLexer):
    """
    For VHDL source code.

    .. versionadded:: 1.5
    """
    name = 'vhdl'
    aliases = ['vhdl']
    filenames = ['*.vhdl', '*.vhd']
    mimetypes = ['text/x-vhdl']
    flags = re.MULTILINE | re.IGNORECASE

    tokens = {
        'root': [
            (r'\n', Text),
            (r'\s+', Text),
            (r'\\\n', Text),  # line continuation
            (r'--.*?$', Comment.Single),
            (r"'(U|X|0|1|Z|W|L|H|-)'", String.Char),
            (r'[~!%^&*+=|?:<>/-]', Operator),
            (r"'[a-z_]\w*", Name.Attribute),
            (r'[()\[\],.;\']', Punctuation),
            (r'"[^\n\\"]*"', String),

            (r'(library)(\s+)([a-z_]\w*)',
             bygroups(Keyword, Text, Name.Namespace)),
            (r'(use)(\s+)(entity)', bygroups(Keyword, Text, Keyword)),
            (r'(use)(\s+)([a-z_][\w.]*\.)(all)',
             bygroups(Keyword, Text, Name.Namespace, Keyword)),
            (r'(use)(\s+)([a-z_][\w.]*)',
             bygroups(Keyword, Text, Name.Namespace)),
            (r'(std|ieee)(\.[a-z_]\w*)',
             bygroups(Name.Namespace, Name.Namespace)),
            (words(('std', 'ieee', 'work'), suffix=r'\b'),
             Name.Namespace),
            (r'(entity|component)(\s+)([a-z_]\w*)',
             bygroups(Keyword, Text, Name.Class)),
            (r'(architecture|configuration)(\s+)([a-z_]\w*)(\s+)'
             r'(of)(\s+)([a-z_]\w*)(\s+)(is)',
             bygroups(Keyword, Text, Name.Class, Text, Keyword, Text,
                      Name.Class, Text, Keyword)),
            (r'([a-z_]\w*)(:)(\s+)(process|for)',
             bygroups(Name.Class, Operator, Text, Keyword)),
            (r'(end)(\s+)', bygroups(using(this), Text), 'endblock'),

            include('types'),
            include('keywords'),
            include('numbers'),

            (r'[a-z_]\w*', Name),
        ],
        'endblock': [
            include('keywords'),
            (r'[a-z_]\w*', Name.Class),
            (r'(\s+)', Text),
            (r';', Punctuation, '#pop'),
        ],
        'types': [
            (words((
                'boolean', 'bit', 'character', 'severity_level', 'integer', 'time',
                'delay_length', 'natural', 'positive', 'string', 'bit_vector',
                'file_open_kind', 'file_open_status', 'std_ulogic', 'std_ulogic_vector',
                'std_logic', 'std_logic_vector', 'signed', 'unsigned'), suffix=r'\b'),
             Keyword.Type),
        ],
        'keywords': [
            (words((
                'abs', 'access', 'after', 'alias', 'all', 'and',
                'architecture', 'array', 'assert', 'attribute', 'begin', 'block',
                'body', 'buffer', 'bus', 'case', 'component', 'configuration',
                'constant', 'disconnect', 'downto', 'else', 'elsif', 'end',
                'entity', 'exit', 'file', 'for', 'function', 'generate',
                'generic', 'group', 'guarded', 'if', 'impure', 'in',
                'inertial', 'inout', 'is', 'label', 'library', 'linkage',
                'literal', 'loop', 'map', 'mod', 'nand', 'new',
                'next', 'nor', 'not', 'null', 'of', 'on',
                'open', 'or', 'others', 'out', 'package', 'port',
                'postponed', 'procedure', 'process', 'pure', 'range', 'record',
                'register', 'reject', 'rem', 'return', 'rol', 'ror', 'select',
                'severity', 'signal', 'shared', 'sla', 'sll', 'sra',
                'srl', 'subtype', 'then', 'to', 'transport', 'type',
                'units', 'until', 'use', 'variable', 'wait', 'when',
                'while', 'with', 'xnor', 'xor'), suffix=r'\b'),
             Keyword),
        ],
        'numbers': [
            (r'\d{1,2}#[0-9a-f_]+#?', Number.Integer),
            (r'\d+', Number.Integer),
            (r'(\d+\.\d*|\.\d+|\d+)E[+-]?\d+', Number.Float),
            (r'X"[0-9a-f_]+"', Number.Hex),
            (r'O"[0-7_]+"', Number.Oct),
            (r'B"[01_]+"', Number.Bin),
        ],
    }
