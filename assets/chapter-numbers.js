/*
 * 章番号の自動付与 (右下のスライド番号用)
 *
 * 横方向のスライドを「章」とみなし、各スライドに番号を割り当てる。見出しには表示しない。
 *   - 縦に並んだスライド (章の中のスライド): 「章-連番」 例) 3-1, 3-2
 *   - 縦スライドを持たない横スライド: 「章」 例) 4
 *   - 1枚目 (タイトルスライド) と、見出しの無いスライドは連番を消費しない (右下は章番号のみ)
 *   - 連番から外したいスライドには data-no-number 属性を付ける
 *
 * Reveal.initialize() より前に読み込み、slideNumber: chapterSlideNumber を指定する。
 */
(function () {
    // 番号を割り当てたら true を返す
    function numberHeading(slide, label) {
        slide.dataset.chapterNumber = label.split('-')[0]; // 見出しが無くても右下には章番号を出す
        if (slide.hasAttribute('data-no-number')) return false;
        if (!slide.querySelector('h2, h1')) return false;
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
