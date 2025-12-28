

<h1>TXT → CSV → MySQL Data Parsing Project</h1>

<p>
This project demonstrates how to convert <strong>unstructured and broken TXT data</strong>
into a <strong>clean CSV file</strong> and then store it reliably in a
<strong>MySQL database</strong> using Python.
</p>

<hr>

<h2>1. Problem Statement</h2>

<p>The input data is inconsistent and broken across multiple lines:</p>

<pre>
Suresh Sharma | suresh.sharma1@example.com | 9276756702 | House 224,
Pune, India | 105255 Pooja Patel | pooja.patel2@example.com | 9627845077
| House 274, Pune, India | 28026
</pre>

<ul>
    <li>Records are not on single lines</li>
    <li>Addresses contain commas and line breaks</li>
    <li>Only the pipe character <code>|</code> is consistent</li>
</ul>

<p>
Traditional line-based parsing fails.  
This project solves the problem using <strong>pattern-based parsing</strong>.
</p>

<hr>

<h2>2. Core Idea of the Solution</h2>

<div class="note">
<strong>Important Concept:</strong><br>
The solution does <em>NOT</em> rely on line breaks.<br>
It relies entirely on a repeating data pattern:
<br><br>
<code>Name | Email | Phone | Address | PostalCode</code>
</div>

<p>
Once this structure is identified, the data can be extracted safely regardless of formatting.
</p>

<hr>

<h2>3. Why We Remove Newlines</h2>

<pre>
raw_text = raw_text.replace("\n", " ")
</pre>

<p>
This converts the entire file into a single continuous string.
</p>

<h3>Why this is safe?</h3>

<ul>
    <li>Addresses may span multiple lines</li>
    <li>Newlines do not represent record boundaries</li>
    <li>The pipe (<code>|</code>) always separates fields</li>
</ul>

<p>
By removing newlines, we prevent accidental record breaks.
</p>

<hr>

<h2>4. Regex Pattern Explained (Most Important Part)</h2>

<pre>
pattern = r'([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*(\d+)'
</pre>

<h3>How Regex Identifies One Record</h3>

<table border="1" cellpadding="8" cellspacing="0">
<tr>
    <th>Regex Part</th>
    <th>Meaning</th>
</tr>
<tr>
    <td><code>[^|]+</code></td>
    <td>Capture everything until the next | symbol</td>
</tr>
<tr>
    <td><code>\s*\|\s*</code></td>
    <td>Match the | symbol with optional spaces</td>
</tr>
<tr>
    <td><code>(\d+)</code></td>
    <td>Postal code (numbers only)</td>
</tr>
</table>

<h3>Why Regex Still Works After Making One Big String</h3>

<p>
Regex scans the string from left to right and looks for this exact pattern:
</p>

<pre>
Text | Text | Text | Text | Number
</pre>

<p>
Once found, it stores it as <strong>one complete record</strong> and continues scanning
for the next occurrence.
</p>

<hr>

<h2>5. How Records Are Extracted</h2>

<pre>
records = re.findall(pattern, raw_text)
</pre>

<p>
This produces a list of tuples:
</p>

<pre>
[
 ('Suresh Sharma', 'suresh.sharma1@example.com', '9276756702',
  'House 224, Pune, India', '105255'),
 ('Pooja Patel', 'pooja.patel2@example.com', '9627845077',
  'House 274, Pune, India', '28026')
]
</pre>

<p>
Each tuple represents one person.
</p>

<hr>

<h2>6. Writing Correct CSV</h2>

<pre>
writer.writerow(["Name", "Email", "Phone", "Address", "PostalCode"])
writer.writerow([field.strip() for field in record])
</pre>

<h3>Why CSV is Correct</h3>

<ul>
    <li>Fields are already clean</li>
    <li>Addresses remain intact</li>
    <li>Extra spaces are removed using <code>.strip()</code></li>
    <li>CSV module handles commas safely</li>
</ul>

<hr>

<h2>7. Inserting Data into MySQL</h2>

<pre>
INSERT INTO users (name, email, phone, address, postal_code)
VALUES (%s, %s, %s, %s, %s)
</pre>

<pre>
cursor.executemany(insert_query, records)
</pre>

<h3>Why This Is Safe</h3>

<ul>
    <li>Uses parameterized queries</li>
    <li>Prevents SQL injection</li>
    <li>Fast bulk insertion</li>
    <li>Matches CSV structure exactly</li>
</ul>

<hr>

<h2>8. Project Flow Summary</h2>

<ol>
    <li>Read raw TXT file</li>
    <li>Remove line breaks</li>
    <li>Extract records using regex pattern</li>
    <li>Write clean CSV</li>
    <li>Insert into MySQL database</li>
</ol>

<hr>

<h2>9. Key Learnings</h2>

<ul>
    <li>Regex works on patterns, not lines</li>
    <li>Reliable delimiters matter more than formatting</li>
    <li>Data cleaning should be structure-driven</li>
    <li>One clean extraction can feed multiple systems</li>
</ul>

<hr>

<h2>10. Conclusion</h2>

<p>
This project demonstrates a real-world, production-ready approach to parsing broken text data.
By focusing on structure instead of formatting, we achieve accuracy, scalability, and reliability.
</p>

<p><strong>Regex + Structure = Clean Data</strong></p>

</body>
</html>
