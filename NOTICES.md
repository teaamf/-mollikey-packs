# Notices

Where the data in these packs comes from, and the notices its licences ask for.

## Chinese Pinyin dictionary (`packs/chinese-pinyin.mollikey`)

The pack is licensed **CC BY-SA 4.0** (https://creativecommons.org/licenses/by-sa/4.0/). It is built by
`tools/build_pinyin_pack.py` from:

- **CC-CEDICT** (release of 2023-11-07), published by MDBG, licensed CC BY-SA 4.0. It is based on CEDICT, Copyright (C)
  1997, 1998 Paul Andrew Denisowski. https://www.mdbg.net/chinese/dictionary?page=cc-cedict. Used for which pinyin
  goes with which word: the simplified headwords and their pinyin, tones removed.
- **jieba**'s `dict.txt`, Copyright (c) 2013 Sun Junyi, MIT licence. https://github.com/fxsjy/jieba. Used for how
  often each word is used, scaled to the pack's weights. Its licence:

```
The MIT License (MIT)

Copyright (c) 2013 Sun Junyi

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

Changes made: entries were filtered (Chinese characters only; entries that are only a variant left out), pinyin was
written without tones and spaces (ü as v), frequencies were rescaled, and minor readings of characters were weighted
lower. The same notices are at the top of the dictionary file inside the pack.

## Runes (example) (`packs/runes-example.mollikey`)

Made for MolliKey; CC0 1.0.
