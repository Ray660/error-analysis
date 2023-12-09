let selectsContainer = document.getElementById('selectsContainer');
let addOption = document.getElementById('addOption');
let scriptMode = null;
const type = document.querySelector('.num').textContent.trim().substring(0, 2)

// 在页面加载时调用函数
window.onload = setHeightToWidth;
// 当窗口大小改变时，再次调用函数
window.onresize = setHeightToWidth;
window.onchange = setHeightToWidth;

// add select
addOption.addEventListener("click", function (event) {
    event.preventDefault();
    var newSelectNum = selectsContainer.children.length + 1; // 计算新的选项编号

    var newSelect = document.createElement('div');
    newSelect.classList.add('select');
    var selectId = `select${newSelectNum}0`
    newSelect.innerHTML = `
        <div class="num">${type + newSelectNum}</div>
        <div class="insertCase">
            <textarea class="selectInput" placeholder="请输入选项内容" id=${selectId} name=${selectId}></textarea>
        </div>
        <div class="dele"><a href="#" class="delOption">删除</a></div>
    `;

    selectsContainer.appendChild(newSelect); // 将新创建的选择项添加到容器中
    event.stopPropagation()
});

// 使用事件委托监听所有textarea的focus事件
var lastFocusedTextarea = null;
document.body.addEventListener('focus', function (event) {
    if (event.target.tagName === 'TEXTAREA' || event.target.isContentEditable) {
        lastFocusedTextarea = event.target;
    }
}, true); // 使用事件捕获


// 监听特殊符号的点击事件
let specialSymbols = document.querySelector(".special_symbols");
specialSymbols.addEventListener('click', function (event) {
    event.preventDefault(); // 防止默认的链接行为

    if (lastFocusedTextarea) {
        if (event.target && event.target.className === "insertSymbol") {
            var symbolText = event.target.textContent; // 获取符号文本
            insertAtCursor(lastFocusedTextarea, symbolText); // 在光标位置插入符号
        }
        else if (event.target && event.target.className === "superscript") {
            toggleScript(event, 'superscript');
        }
        else if (event.target && event.target.className === "subscript") {
            toggleScript(event, 'subscript');
        }
        else if (event.target && event.target.className === "insertEmpty") {
            toggleScript(event, 'insertEmpty');
        }
        else if (event.target && event.target.id === "insertText") {
            var parent = lastFocusedTextarea.parentElement;
            if (parent.classList.length === 0) {
                parent = parent.parentElement
            }
            var childNode = document.createElement("div");
            childNode.style.width = "100%";
            childNode.style.height = "auto";
            if (parent.className === "topic_input") {
                var childId = document.querySelectorAll(".topic_input .topicInput").length;
                childNode.innerHTML = `
                <textarea class="topicInput" id="topic${childId}" name="topic${childId}" placeholder="请输入题目"></textarea>
                <p><a class="deleteText" href="#" style="margin-left: 2em;">删除文本域</a></p>
                `
                parent.appendChild(childNode);
                childNode.focus();
            } else if (parent.className === "insertCase") {
                var selectId = document.querySelectorAll(".selects .select").length;
                var childId = parent.querySelectorAll(".selectInput").length;
                childNode.innerHTML = `
                <textarea class="selectInput" id="select${selectId}${childId}" name="select${selectId}${childId}" placeholder="请输入选项内容"></textarea>
                <p><a class="deleteText" id="${childNode.id}del" href="#">删除文本域</a></p>
                `
                parent.appendChild(childNode);
                childNode.focus();
            }
        }
        else if (event.target && event.target.id === "insertImage") {
            if (lastFocusedTextarea.isContentEditable) {
                let explain = document.querySelector('.explain');
                let newQorE = createNewNode(explain, 'image', null);
                const imgIndex = document.querySelectorAll('.newQorE').length;
                newQorE.querySelector('p').innerHTML = `
                <input type="file" class="explainInput" id="img${imgIndex}" name="img${imgIndex}" style="display: none" accept="image/*">
                <img id="img${imgIndex}Preview" style="width: 60%; height: auto; display: none" src="#">
                `
                previewImg(newQorE);
            }

            var parent = lastFocusedTextarea.parentElement;
            if (parent.classList.length === 0) {
                parent = parent.parentElement
            }
            var childNode = document.createElement("div");
            childNode.style.width = "100%";
            childNode.style.height = "auto";
            if (parent.className === "topic_input") {
                var childId = document.querySelectorAll(".topic_input .topicInput").length;
                childNode.innerHTML = `
                <input type="file" class="topicInput" id="topic${childId}" name="topic${childId}" style="display: none" accept="image/*">
                <img id="topic${childId}Preview" name="topic${childId}Preview" style="width: 60%; height: auto; display: none" src="#">
                <a class="deleteImage" id="topic${childId}del" href="#" style="display: none">删除图片</a>
                `
                parent.appendChild(childNode);
                previewImg(childNode);
            } else if (parent.className === "insertCase") {
                var selectId = document.querySelectorAll(".selects .select").length;
                var childId = parent.querySelectorAll(".selectInput").length;
                childNode.innerHTML = `
                <input type="file" class="selectInput" id="select${selectId}${childId}" name="select${selectId}${childId}" accept="image/*" style="display: none">
                <img id="select${childId}Preview" name="select${childId}Preview" style="width: 60%; height: auto; display: none" src="#">
                <a class="deleteImage" id="select${selectId}${childId}del" href="#" style="display: none">删除图片</a>
                `
                parent.appendChild(childNode);
                previewImg(childNode);
            }
        }
    }
})

// 删除数据
document.body.addEventListener('click', function (event) {
    if (event.target.matches('.deleteText')) {
        event.preventDefault();
        const divToRemove = event.target.closest('div');
        if (divToRemove) {
            divToRemove.remove();
        }
        updateDate()
    }
    if (event.target.matches('.deleteImage')) {
        event.preventDefault();
        const divToRemove = event.target.closest('div');
        if (divToRemove) {
            divToRemove.remove();
        }
        updateDate()
    }
    if (event.target.matches('.delOption')) {
        event.preventDefault();
        const divToRemove = event.target.closest('.select');
        if (divToRemove) {
            divToRemove.remove();
        }
        updateDate()
    }
});

// 提交时核查topic不为空
document.querySelector('.redirect_button input').addEventListener('click', function (event) {
    console.log("我点击了提交按钮")
    const topicInput = document.querySelector('.topic_input')
    const innerTextareas = topicInput.querySelectorAll('textarea')
    console.log(`获取topicInput:${topicInput} and innerTextareas:${innerTextareas}`)
    innerTextareas.forEach(function (innerTextarea, index) {
        if (!innerTextarea.value.trim()) {
            event.preventDefault();
            alert("不能提交空的题目")
        }
    })
    event.stopPropagation()
})
document.querySelector('.redirect_button a').addEventListener('click', (event) => {
    event.stopPropagation()
})


function setHeightToWidth() {
    var elements = document.querySelectorAll('.button .special_symbols .symbol');

    elements.forEach(function (element) {
        var width = element.offsetWidth; // 获取元素的宽度
        element.style.height = width + 'px'; // 设置高度等于宽度
    });
}

function previewImg(childNode) {
    var imgInput = childNode.querySelector("input")
    imgInput.click()
    imgInput.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function (e) {
                var imagePreview = childNode.querySelector("img")
                var deleteImage = childNode.querySelector('.deleteImage')
                imagePreview.style.display = "block";
                imagePreview.src = `${e.target.result}`;
                deleteImage.style.display = "block";
            };
            reader.readAsDataURL(file);
        }
        event.stopPropagation()
    })
}

function insertAtCursor(element, text) {
    let startPos, endPos, range, sel;

    if (element.tagName === 'TEXTAREA' || element.tagName === 'INPUT') {
        startPos = element.selectionStart;
        endPos = element.selectionEnd;
        element.value = element.value.substring(0, startPos)
            + text
            + element.value.substring(endPos, element.value.length);
        element.selectionStart = element.selectionEnd = startPos + text.length;
    } else if (element.isContentEditable) {
        sel = window.getSelection();
        if (sel.rangeCount > 0) {
            console.log(`此时有${sel.rangeCount}个range对象`)
            range = sel.getRangeAt(0); // 选中内容
            range.deleteContents(); // 清除选中内容

            let textNode = document.createTextNode(text); // 创建一个文本元素
            range.insertNode(textNode);

            // 移动光标到插入文本之后
            range = range.cloneRange();
            range.selectNodeContents(textNode); // 重新选择选中内容
            range.collapse(false); // 将光标移到选中内容结尾处
            sel.removeAllRanges(); // 清除Selection中的所有range
            sel.addRange(range); // 重新插入range，使光标在range的后面
        }
    }

    element.focus();
}

function insertHtmlAtCursor(element, html) {
    let range, sel;
    if (element.isContentEditable) {
        sel = window.getSelection();
        if (sel.rangeCount > 0) {
            range = sel.getRangeAt(0);
            range.deleteContents();

            // 创建一个临时的 div 来容纳 HTML
            let tempDiv = document.createElement("span");
            tempDiv.innerHTML = html;
            let frag = document.createDocumentFragment(), child;
            while ((child = tempDiv.firstChild)) {
                frag.appendChild(child);
            }

            // 插入 HTML 片段
            range.insertNode(frag);

            // 移动光标到插入内容之后
            range = range.cloneRange();
            range.setStartAfter(frag);
            range.collapse(true);
            sel.removeAllRanges();
            sel.addRange(range);
        }
    }

    element.focus();
}

function toggleScript(event, type) {
    if (lastFocusedTextarea) {
        if (lastFocusedTextarea.tagName === 'TEXTAREA' || lastFocusedTextarea.tagName === 'INPUT') {
            var selectedText = lastFocusedTextarea.value.substring(lastFocusedTextarea.selectionStart, lastFocusedTextarea.selectionEnd);
            if (selectedText.length > 0) {
                let scriptText;
                if (type === 'superscript') {
                    scriptText = '<sup>' + selectedText + '</sup>';
                } else {
                    scriptText = '<sub>' + selectedText + '</sub>';
                }
                if (type === 'insertEmpty') {
                    if (lastFocusedTextarea.parentElement.className === 'insertCase' || lastFocusedTextarea.parentElement.parentElement.className === 'insertCase') {
                        scriptText = '<input type="text" size="请在这里填入预计文字长度" >';
                    }
                }
                insertAtCursor(lastFocusedTextarea, scriptText);
            } else {
                let text;
                if (type === 'insertEmpty') {
                    if (lastFocusedTextarea.parentElement.className === 'insertCase' || lastFocusedTextarea.parentElement.parentElement.className === 'insertCase') {
                        text = '<input type="text" size="请在这里填入预计文字长度" >';
                        insertAtCursor(lastFocusedTextarea, text);
                    }
                } else if (scriptMode === type) {
                    scriptMode = null;
                    if (type === 'superscript') {
                        text = '</sup>'
                    } else if (type === 'subscript') {
                        text = '</sub>'
                    }
                    insertAtCursor(lastFocusedTextarea, text);
                } else {
                    scriptMode = type;
                    if (type === 'superscript') {
                        text = '<sup>'
                    } else {
                        text = '<sub>'
                    }
                    ;
                    insertAtCursor(lastFocusedTextarea, text);
                }
            }
        } else if (lastFocusedTextarea.isContentEditable) {
            let newTab;

            if (type === 'subscript') {
                newTab = document.createElement('sub')
            } else {
                newTab = document.createElement('sup')
            }
            ;

            const sel = window.getSelection();
            const range = sel.getRangeAt(0);
            if (!range.collapsed) {
                const text = range.toString();
                range.deleteContents();
                newTab.textContent = text;

            } else {
                newTab.textContent = 'n';
            }
            range.insertNode(newTab);
        }
    }
}

function cursorFocus(element) {
    // 创建一个 Range 对象
    var range = document.createRange();
    var sel = window.getSelection();

    // 将 range 的起始和结束位置都设置为 lastSpan 的最后
    range.selectNodeContents(element);
    range.collapse(false); // false 表示范围折叠到结束位置

    // 清除当前任何选区，然后将新的 range 添加到选区中
    sel.removeAllRanges();
    sel.addRange(range);

    // 聚焦到元素
    element.focus();
}

function updateDate() {
    updateSelectNumbers();
    updateTopicName();
}

function updateSelectNumbers() {
    var selects = document.querySelectorAll('#selectsContainer .select');
    selects.forEach(function (select, index) {
        var numElement = select.querySelector('.num');
        var insertCase = select.querySelector('.insertCase');
        numElement.textContent = type + (index + 1);
        updateSelectInputId(index, insertCase); // 更新textarea和image的id以及name
    });
}

function updateSelectInputId(selectNum, insertCase) {
    var selectInputs = insertCase.querySelectorAll('.selectInput')
    selectInputs.forEach(function (selectInput, index) {
        selectInput.id = `select${selectNum + 1}${index}`
        selectInput.name = selectInput.id
    })
}

function updateTopicName() {
    var allTopicInput = document.querySelectorAll(".topicInput");
    allTopicInput.forEach(function (date, index) {
        date.id = `topic${index}`;
        date.name = date.id;
    });
}
