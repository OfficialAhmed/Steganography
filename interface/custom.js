function is_input_valid(msg, img, pswd, key) {
    // Check all user inputs before trying to encode or decode

    var err = ''
    if (msg.length >= 1) {
        if (pswd.length == 16) {
            if (img) {
                if (key) {
                    Swal.fire(
                        'PLEASE WAIT!',
                        'Encoding in progress...',
                        'success'
                    )
                    return True
                } else
                    err = 'Key cannot be empty'
            } else
                err = 'image cannot be empty'
        } else
            err = 'password must be a length of 16'
    } else
        err = 'text cannot be empty!'

    Swal.fire(
        'INVALID INPUT!',
        err,
        'error'
    )
    return false;
}

function encode_text() {
    let img = document.getElementById('text_encode_input').value
    let password = document.getElementById('text_encode_pass').value
    let message = document.getElementById('text_encode_message').value

    if (is_input_valid(message, img, password, 'pass')) {
        // encode message through eel Python
    }

}

function decode_text() {
    let key = document.getElementById('text_decode_key').value
    let img = document.getElementById('text_decode_input').value
    let password = document.getElementById('text_decode_pass').value
    let message = document.getElementById('text_decode_message').value

    if (is_input_valid(message, img, password, key)) {
        // encode message through eel Python
    }
}

function encode_image() {
    alert("Encoding image...");
}

function decode_image() {
    alert("Decoding image...");
}


function preview_image(input, output) {
    const imageInput = document.getElementById(input);
    const imagePreview = document.getElementById(output);

    imageInput.addEventListener('change', function () {
        const file = this.files[0];

        if (file) {
            const reader = new FileReader();

            reader.addEventListener('load', function () {
                imagePreview.innerHTML = `<img src="${this.result}" alt="Image Preview">`;
            });

            reader.readAsDataURL(file);
        }
    });

}

function type_writter() {
    // Generated query code to animate the title
    var items = document.querySelectorAll('#title_type');
    for (var i = 0, len = items.length; i < len; i++) {
        (function () {
            var e = this, t = JSON.parse('["Stagn","Stegnoph","Stegnography"]'), r = function (e) { return parseInt(e, 10) || 0 }, n = function (e) { return !!e }, o = function () { var o = e; o.innerHTML = '<span></span>'; var c = parseInt('Infinity', 10), s = { typeSpeed: r('100'), startDelay: r(''), backDelay: r('700'), backSpeed: r(''), smartBackspace: n('true'), fadeOut: n(''), fadeOutClass: 'typed-fade-out', fadeOutDelay: r('500'), shuffle: n(''), loop: n(''), loopCount: isNaN(c) ? 1 / 0 : c, showCursor: n(''), cursorChar: '|', autoInsertCss: n('true'), bindInputFocusEvents: n(''), attr: '', contentType: 'html' }; t && t.length && (s.strings = t), new Typed(o.children[0], s) }; if (window.Typed) o(); else { var c = document.createElement('script'); c.src = 'https://cdn.jsdelivr.net/npm/typed.js@2.0.11', c.onload = o, document.head.appendChild(c) }
        }.bind(items[i]))();
    }
    var props = { "ipss3h": { "classactive": "tab-active", "selectortab": "aria-controls" }, "iy8t4q": { "classactive": "tab-active", "selectortab": "aria-controls" }, "ibj7j1": { "classactive": "tab-active", "selectortab": "aria-controls" } };
    var ids = Object.keys(props).map(function (id) { return '#' + id }).join(',');
    var els = document.querySelectorAll(ids);
    for (var i = 0, len = els.length; i < len; i++) {
        var el = els[i];
        (function (t) { var e, n, r = this, o = t.classactive, a = t.selectortab, c = window, i = c.history, s = c._isEditor, b = '[role=tab]', p = document, l = p.body, u = p.location, f = l.matchesSelector || l.webkitMatchesSelector || l.mozMatchesSelector || l.msMatchesSelector, y = function (t, e) { for (var n = t || [], r = 0; r < n.length; r++)e(n[r], r) }, d = function (t) { return t.getAttribute(a) }, O = function (t, e) { return t.querySelector(e) }, g = function () { return r.querySelectorAll(b) }, j = function (t, e) { return !s && (t.tabIndex = e) }, h = function (t) { y(g(), (function (t) { t.className = t.className.replace(o, '').trim(), t.ariaSelected = 'false', j(t, '-1') })), y(r.querySelectorAll("[role=tabpanel]"), (function (t) { return t.hidden = !0 })), t.className += ' ' + o, t.ariaSelected = 'true', j(t, '0'); var e = d(t), n = e && O(r, "#".concat(e)); n && (n.hidden = !1) }, v = O(r, ".".concat(o).concat(b)); (v = v || (n = (u.hash || '').replace('#', '')) && O(r, (e = a, "".concat(b, "[").concat(e, "=").concat(n, "]"))) || O(r, b)) && h(v), r.addEventListener('click', (function (t) { var e = t.target, n = f.call(e, b); if (n || (e = function (t) { var e; return y(g(), (function (n) { e || n.contains(t) && (e = n) })), e }(e)) && (n = 1), n && !t.__trg && e.className.indexOf(o) < 0) { t.preventDefault(), t.__trg = 1, h(e); var r = d(e); try { i && i.pushState(null, null, "#".concat(r)) } catch (t) { } } })) }.bind(el))(props[el.id]);
    }
}

window.onload = type_writter;