# word-list-json

> List of [English words](https://github.com/atebits/Words/blob/master/Words/en.txt)

Useful if you're creating a word game or just want some words to work with.

Used by [name-me](https://github.com/calvinmetcalf/name-me).


## Install

```bash
$ npm install --save word-list-json
```


## Usage

```js
// a json array of words
var wordList = require('word-list-json');
```
wordlist is sorted by length, in addition to the usual length property the array also has a 'lengths' property which is a dict with keys of word lengths and values which are the array index after the last word of that length e.g. what the array length would be if it had no words with a longer length.


## License

[MIT](http://opensource.org/licenses/MIT) © [Sindre Sorhus](http://sindresorhus.com)
