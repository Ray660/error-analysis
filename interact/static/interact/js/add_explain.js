const params = new URLSearchParams(window.location.search);
let topicType = params.get('type');


// 点击“增加讲解”链接，将增加讲解页面覆盖在input页面上
document.querySelector("#add_explain").addEventListener("click", (event) => {
//     取消链接跳转
    event.preventDefault();
    let parentElement = document.querySelector(".inputBox div");
    if (containsClass(parentElement, 'explainBox')) {
        document.querySelector('.explainBox').style.display = 'flex';
        parentElement.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
        parentElement.style.right = 0;
        parentElement.style.bottom = 0;
    } else {
//     创建讲解页面
        const explainBox = createExplain();
        console.log("成功创建讲解页面")
//     添加讲解页面
        addExplain(explainBox);
        console.log("成功添加讲解页面");
    }
//     文和空插入框隐身
    let empty = document.querySelector('.insertEmpty').parentElement;
    let text = document.querySelector('#insertText').parentElement;
    if (empty) {
        empty.style.display = "none";
    }
    text.style.display = "none";
})
// 思考题和讲解框的插入和关闭
document.querySelector('.inputBox').addEventListener('click', function (event) {
    const explain = document.querySelector('.explain');
//  插入思考题和讲解以及删除
    if (event.target.id === 'addQuestion') {
        event.preventDefault();
        createNewNode(explain, 'question', '新的思考题...');
    }

    if (event.target.id === 'addExplanation') {
        event.preventDefault();
        createNewNode(explain, 'explanation', '新的讲解...');
    }

    if (event.target.className === 'deleteQorE') {
        event.preventDefault();
        event.target.closest('.newQorE').remove();
    }
//  关闭讲解页面
    if (event.target.parentElement.className === 'closeBox') {
        event.preventDefault();
        event.target.closest('.explainBox').style.display = 'none';
        document.querySelector(".inputBox div").style.backgroundColor = "initial";
        document.querySelector(".inputBox div").style.right = "initial";
        document.querySelector(".inputBox div").style.bottom = "initial";
        //     文和空插入框现身
        let empty = document.querySelector('.insertEmpty').parentElement;
        let text = document.querySelector('#insertText').parentElement;
        if (empty) {
            empty.style.display = "flex";
        }
        text.style.display = "flex";
    }
});

// 键盘事件
document.body.addEventListener('keydown', event => {
    console.log(event.key);
    if (event.target.classList.contains('editedSpan') && event.key === 'Enter') {
        event.preventDefault();

        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            range.deleteContents();

            // 创建新的 p 元素
            let html = `${range.toString()}`;
            const newP = createP(html);

            // 判断触发事件的元素位于其父元素的何处
            insertSpan(event.target.closest('p'), newP);

            // 将当前位置之后的所有内容移动到新的 span 中
            const clonedRange = range.cloneRange();
            clonedRange.selectNodeContents(event.target);
            clonedRange.setStart(range.endContainer, range.endOffset);
            let newSpan = newP.querySelector('span');
            newSpan.appendChild(clonedRange.extractContents());

            // 将光标移动到新标签中文本的开头
            moveCursorToElement(newSpan, 'start');
        }
    }
    if (event.target.isContentEditable && event.key === 'ArrowRight') {
        const selection = window.getSelection();
        if (selection.rangeCount === 0) return;

        const range = selection.getRangeAt(0);
        let currentElement = range.endContainer;

        // 检查光标是否位于元素（或子元素）的末尾
        if (range.collapsed && range.endOffset === currentElement.textContent.length) {
            let hasFollowingSiblings = false;

            // 如果当前元素是文本节点并且有父元素，将当前元素设置为其父元素
            if (currentElement.nodeType === Node.TEXT_NODE && currentElement.parentNode) {
                currentElement = currentElement.parentNode;
            }

            let sibling = currentElement.nextSibling;
            while (sibling) {
                if (sibling.nodeType === Node.ELEMENT_NODE || (sibling.nodeType === Node.TEXT_NODE && sibling.textContent.trim() !== '')) {
                    hasFollowingSiblings = true;
                    break;
                }
                sibling = sibling.nextSibling;
            }

            if (!hasFollowingSiblings) {
                // 在最近的父级 <p> 标签下添加 span
                const parentParagraph = currentElement.closest('p');
                if (parentParagraph) {
                    const newSpan = createEditedSpan();
                    parentParagraph.appendChild(newSpan);
                    moveCursorToElement(newSpan, 'start');
                }
            }
        }
    }


});

// 点击事件


function containsClass(parentElement, className) {
    return parentElement.querySelector('.' + className) !== null;
}

function createExplain() {
    let answer;
    if (topicType === 's') {
        answer =
            `<select name="judge" id="id_judge">
                <option value="unknown">未知</option>
                <option value="true">是</option>
                <option value="false" selected="">否</option>
            </select>`;
    } else if (topicType === 'c') {
        answer = `<input name="fill" id="id_fill" size="30">`;
    } else if (topicType === 'w') {
        answer = `<div contenteditable="true" style="width: 30em; border: 1px solid gray;"></div>`
    }

    let explainBox = document.createElement("div");
    explainBox.classList.add("explainBox");
    explainBox.innerHTML = `
    <div class="closeBox"><a href="#"></a></div>
    <div class="correctAnswer">
        <h3 class="prompt">正确答案：</h3>
        ${answer}
    </div>
    <div class="selectExplain">
        <h3 class="prompt">讲解：</h3>
        <div class="explain">
            <a href="#" id="addQuestion">+思考题</a>
            <a href="#" id="addExplanation">+讲解</a>

        </div>
    </div>
    `
    return explainBox;
}

function addExplain(explainBox) {
    let parentElement = document.querySelector(".inputBox div");
    parentElement.appendChild(explainBox);
    parentElement.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    parentElement.style.right = 0;
    parentElement.style.bottom = 0;
}


function createNewNode(parent, className, placeholder) {
    /*
    parent: 要插入新元素的父级元素
    className：创建可编辑span时的新增类名
    placeholder：可编辑span的初始提示词
     */

    let newNode = document.createElement('div');
    newNode.className = 'newQorE';

    const newQuestion = createEditedBox(className, placeholder);
    const delQuestion = createDelBox();
    newNode.appendChild(newQuestion);
    newNode.appendChild(delQuestion);

    parent.appendChild(newNode);
    return newNode;
}

function createEditedBox(className, placeholder) {
    let newEditedBox = document.createElement('div');
    newEditedBox.className = className;
    newEditedBox.appendChild(createP(placeholder))
    return newEditedBox;
}

function createP(placeholder) {
    let newP = document.createElement('p');
    newP.appendChild(createEditedSpan(null, placeholder));
    return newP;
}

function createEditedSpan(className = null, placeholder = null) {
    let newEditedSpan = document.createElement('span');
    newEditedSpan.classList.add('editedSpan');
    if (className) {
        newEditedSpan.classList.add(className);
    }
    newEditedSpan.contentEditable = 'true';
    if (typeof placeholder === "string") {
        newEditedSpan.textContent = placeholder;
    } else if (placeholder instanceof HTMLElement) {
        newEditedSpan.appendChild(placeholder);
    }
    return newEditedSpan;
}

function createDelBox() {
    let newDelBox = document.createElement('a');
    newDelBox.className = 'deleteQorE';
    newDelBox.href = '#';
    newDelBox.textContent = '删除';
    return newDelBox
}

function moveCursorToElement(element, endOrStart = 'end') {
    if (!(element instanceof HTMLElement)) {
        console.error("传入的对象不是有效的DOM元素");
        return;
    }

    const selection = window.getSelection();
    const range = document.createRange();

    // 检查元素是否为空
    if (element.textContent === '') {
        // 对于空元素，将range的起点和终点都设置为该元素
        range.setStart(element, 0);
        range.setEnd(element, 0);
    } else {
        // 选择element的内容
        range.selectNodeContents(element);
        if (endOrStart === 'end') {
            range.collapse(false);
        } else if (endOrStart === 'start') {
            range.collapse(true);
        }
    }

    selection.removeAllRanges();
    selection.addRange(range);
}


function insertSpan(element, newSpan) {
    // 判断目标元素位于其父元素的何处
    const parentElement = element.parentElement;
    const nextSibling = element.nextElementSibling;

    if (nextSibling) {
        // 如果有下一个兄弟元素，则在该元素之前插入newSpan
        parentElement.insertBefore(newSpan, nextSibling);
    } else {
        // 如果没有下一个兄弟元素，则说明是最后一个子元素，直接在父元素最后添加
        parentElement.appendChild(newSpan);
    }
}



