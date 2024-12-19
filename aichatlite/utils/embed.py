
class Embed:
    @classmethod
    def audio(cls,url):
        return f'<audio controls><source src="{url}" type="audio/mpeg"></audio>'

    @classmethod
    def image(cls,url):
        return f'<img src="{url}" alt="Image" width="200" height="200">'

    @classmethod
    def video(cls,url):
        return f'<video controls><source src="{url}" type="video/mp4"></video>'

    @classmethod
    def youtube(cls,url):
        '''https://www.youtube.com/embed/LMQ5Gauy17k'''
        return f'<iframe width="400" height="215" src={url} title="YouTube video player" frameborder="0" allow="accelerometer; encrypted-media;"></iframe>'

    @classmethod
    def iframe(cls, url):
        return f'<iframe src="{url}" width="560" height="315" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

    @classmethod
    def link(cls, text, url):
        return f'<a href="{url}" target="_blank">{text}</a>'

    @classmethod
    def code(cls, code, language):
        return f'<pre><code class="language-{language}">{code}</code></pre>'


    @classmethod
    def quote(cls, quote, author):
        return f'<blockquote class="blockquote"><p class="mb-0">{quote}</p><footer class="blockquote-footer">{author}</footer></blockquote>'

    @classmethod
    def divider(cls):
        return '<hr>'

    @classmethod
    def markdown(cls, markdown):
        return f'<div class="markdown-body">{markdown}</div>'

    @classmethod
    def error(cls, message):
        return f'<div class="alert alert-danger" role="alert">{message}</div>'

    @classmethod
    def success(cls, message):
        return f'<div class="alert alert-success" role="alert">{message}</div>'

    @classmethod
    def warning(cls, message):
        return f'<div class="alert alert-warning" role="alert">{message}</div>'

    @classmethod
    def info(cls, message):
        return f'<div class="alert alert-info" role="alert">{message}</div>'

    @classmethod
    def code_block(cls, code, language):
        return f'<pre><code class="language-{language}">{code}</code></pre>'

    @classmethod
    def code_output(cls, output, language):
        return f'<pre><code class="language-{language}">{output}</code></pre>'

    @classmethod
    def code_error(cls, error):
        return f'<pre><code class="language-python">{error}</code></pre>'

    @classmethod
    def code_success(cls, message):
        return f'<pre><code class="language-python">{message}</code></pre>'

    @classmethod
    def code_warning(cls, message):
        return f'<pre><code class="language-python">{message}</code></pre>'

    @classmethod
    def code_info(cls, message):
        return f'<pre><code class="language-python">{message}</code></pre>'
