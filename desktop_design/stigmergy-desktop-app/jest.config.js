module.exports = {
  testEnvironment: 'jsdom',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.(test|spec).js', '**/?(*.)+(spec|test).js'],
  coverageDirectory: '<rootDir>/coverage',
  collectCoverageFrom: [
    'src/main/**/*.js',
    'src/renderer/**/*.js',
    '!src/main/main.js',
    '!src/main/preload.js'
  ],
  verbose: true,
  transform: {
    '^.+\\.js$': 'babel-jest'
  },
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy'
  }
};