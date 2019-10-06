%#template for the form for a new task
<p>extract summarization from a text:</p>
<form action="/project2" method="post">
  Original Text:
  <br>
  <textarea name="task" cols="100" rows="20"> </textarea>
  <br>
  Summarization size:
  <br>
  <input type="number" name="size" min="50" value="100">
  <br>
  <input type="checkbox" name="embedding">With SentenceEmbedding
  <br>
  <input type="submit" name="save" value="Generate">
</form>
