module.exports = {
  root: true,
  env: {
    node: true
  },
  'extends': [
    'plugin:vue/essential',
    'eslint:recommended'
  ],
  parserOptions: {
    parser: 'babel-eslint'
  },
  rules: {
    'object-curly-spacing': [ 'error', 'always' ],
    'array-bracket-spacing': [ 'error', 'always' ],
    'semi-spacing': [ 'error', { 'before': false, 'after': true } ],
    'space-in-parens': [ 'error', 'always' ],
    'space-before-blocks': 'error',
    'space-infix-ops': 'error',
    'comma-dangle': [ 'error', 'never' ],
    'no-console': [ 'error', { allow: [ 'warn', 'error' ] } ],
    'space-unary-ops': 'error',
    'no-var': 'error',
    'no-alert': 'error',
    'no-param-reassign': 'warn',
    semi: [ 'error', 'never' ],
    quotes: [ 'error', 'single' ],
    eqeqeq: 'warn'
  }
}
