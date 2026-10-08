/*
 * 章番号の自動付与
 *
 * 横方向のスライドを「章」とみなし、各スライドの最初の見出しの先頭に番号を付ける。
 *   - 縦に並んだスライド (章の中のスライド): 「章-連番」 例) 3-1, 3-2
 *   - 縦スライドを持たない横スライド: 「章」 例) 4
 *   - 1枚目 (タイトルスライド) と、見出しの無いスライドには付けない (連番も消費しない)
 *   - 番号を付けたくないスライドには data-no-number 属性を付ける
 *
 * メニュー (目次) にも番号を出すため、Reveal.initialize() より前に読み込むこと。
 * 右下のスライド番号も揃えるには Reveal.initialize() で slideNumber: chapterSlideNumber を指定する。
 */
(function () {
    // 番号を付けたら true を返す
    function numberHeading(slide, label) {
        slide.dataset.chapterNumber = label.split('-')[0]; // 見出しが無くても右下には章番号を出す
        if (slide.hasAttribute('data-no-number')) return false;
        const heading = slide.querySelector('h2, h1');
        if (!heading || heading.querySelector('.chapter-number')) return false;
        const span = document.createElement('span');
        span.className = 'chapter-number';
        span.textContent = label;
        heading.prepend(span);
        slide.dataset.chapterNumber = label;
        return true;
    }

    const chapters = document.querySelectorAll('.reveal .slides > section');
    chapters.forEach((chapter, chapterIndex) => {
        if (chapterIndex === 0) return;
        const pages = chapter.querySelectorAll(':scope > section');
        if (pages.length === 0) {
            numberHeading(chapter, String(chapterIndex));
            return;
        }
        let pageNumber = 1;
        pages.forEach(page => {
            if (numberHeading(page, chapterIndex + '-' + pageNumber)) pageNumber++;
        });
    });

    // Reveal の slideNumber に渡す関数 (右下の番号を見出しと揃える)
    window.chapterSlideNumber = function (slide) {
        return [(slide && slide.dataset.chapterNumber) || ''];
    };
})();
