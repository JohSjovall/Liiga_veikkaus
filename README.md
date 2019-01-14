# Liiga Veikkaus

Runkosarja pitkäveto laskija.

Ohjelman tarkoituksena on pitää kirjaa Liigan sarjataulukko tapahtumista ja ylläpitää pelaajien pisteitä jokaiselta kierokselta.

Ohjelma lähettää pelaajille sähköpostin heidän pisteistä jokaiselta kierokselta

Pelaajat saavat sähköpostitse oman piste historian

```html
<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"></head>
<body>
<style>
table, th, td {
border: 1px solid black;
border-collapse: collapse;
}
th {
text-align: left;
}
</style>
<font face="Arial"><p>Hei <b>PELAAJA1</b></p>
<p>Olet <b>TESTIPELIN</b> pelissa sijalla <b>1</b></p>
<p> </p>
<h3>RUNKOSARJA JA VEIKKAUKSESI: 2019-01-12</h3><table style="width:25%">
<tr align="left">
<th>SIJOITUS</th>
<th>RUNKOSARJA</th>
<th>VEIKKAUKSESI</th>
<th>PISTEET</th>
</tr>
<tr>
<td>1.</td>
<td>KARPAT</td>
<td>TAPPARA</td>
<td>3</td>
</tr>
<tr>
<td>2.</td>
<td>TPS</td>
<td>KARPAT</td>
<td>4</td>
</tr>
<tr>
<td>3.</td>
<td>TAPPARA</td>
<td>TPS</td>
<td>4</td>
</tr>
<tr>
<td>4.</td>
<td>PELICANS</td>
<td>JYP</td>
<td>-4</td>
</tr>
<tr>
<td>5.</td>
<td>LUKKO</td>
<td>HIFK</td>
<td>1</td>
</tr>
<tr>
<td>6.</td>
<td>HPK</td>
<td>PELICANS</td>
<td>3</td>
</tr>
<tr>
<td>7.</td>
<td>SPORT</td>
<td>LUKKO</td>
<td>2</td>
</tr>
<tr>
<td>8.</td>
<td>HIFK</td>
<td>KOOKOO</td>
<td>-3</td>
</tr>
<tr>
<td>9.</td>
<td>SAIPA</td>
<td>ASSAT</td>
<td>-3</td>
</tr>
<tr>
<td>10.</td>
<td>ILVES</td>
<td>ILVES</td>
<td>4</td>
</tr>
<tr>
<td>11.</td>
<td>JYP</td>
<td>SPORT</td>
<td>-1</td>
</tr>
<tr>
<td>12.</td>
<td>KALPA</td>
<td>HPK</td>
<td>-3</td>
</tr>
<tr>
<td>13.</td>
<td>JUKURIT</td>
<td>JUKURIT</td>
<td>3</td>
</tr>
<tr>
<td>14.</td>
<td>KOOKOO</td>
<td>SAIPA</td>
<td>-2</td>
</tr>
<tr>
<td>15.</td>
<td>ASSAT</td>
<td>KALPA</td>
<td>0</td>
</tr></table>

<p>KUUSI OIKEIN PISTE: 0</p>
<p>KOKONAISPISTEET: <b>8</b></p>
<p> </p>
<h3>HISTORIASI</h3>
<table table="" style="width:80%">
<tr align="left">
<th>PAIVAMAARA</th>
<th>HPK</th>
<th>HIFK</th>
<th>ILVES</th>
<th>JUKURIT</th>
<th>JYP</th>
<th>KALPA</th>
<th>KOOKOO</th>
<th>KARPAT</th>
<th>LUKKO</th>
<th>PELICANS</th>
<th>SAIPA</th>
<th>SPORT</th>
<th>TAPPARA</th>
<th>TPS</th>
<th>ASSAT</th>
<th>KUUSI_OIKEIN</th>
<th>KOKONAISPISTEET</th>
</tr>
<tr>
<td>2019-01-12</td>
<td align:?center?="">-3</td>
<td>1</td>
<td>4</td>
<td>3</td>
<td>-4</td>
<td>0</td>
<td>-3</td>
<td>4</td>
<td>2</td>
<td>3</td>
<td>-2</td>
<td>-1</td>
<td>3</td>
<td>4</td>
<td>-3</td>
<td>0</td>
<td>8</td>
</tr>
<tr>
<td>2019-01-11</td>
<td align:?center?="">-3</td>
<td>2</td>
<td>4</td>
<td>3</td>
<td>-5</td>
<td>-1</td>
<td>-3</td>
<td>4</td>
<td>1</td>
<td>4</td>
<td>-3</td>
<td>1</td>
<td>3</td>
<td>4</td>
<td>-3</td>
<td>0</td>
<td>8</td>
</tr>
<tr>
<td>2019-01-10</td>
<td align:?center?="">-3</td>
<td>2</td>
<td>3</td>
<td>3</td>
<td>-5</td>
<td>-1</td>
<td>-3</td>
<td>4</td>
<td>2</td>
<td>3</td>
<td>-1</td>
<td>0</td>
<td>3</td>
<td>4</td>
<td>-3</td>
<td>0</td>
<td>8</td>
</tr>
<tr>
<td>2019-01-06</td>
<td align:?center?="">-3</td>
<td>2</td>
<td>3</td>
<td>3</td>
<td>-5</td>
<td>-1</td>
<td>-3</td>
<td>4</td>
<td>2</td>
<td>3</td>
<td>-1</td>
<td>0</td>
<td>3</td>
<td>4</td>
<td>-3</td>
<td>0</td>
<td>8</td>
</tr>
<tr>
<td>2019-01-05</td>
<td align:?center?="">-3</td>
<td>0</td>
<td>4</td>
<td>2</td>
<td>-6</td>
<td>-1</td>
<td>-1</td>
<td>4</td>
<td>2</td>
<td>3</td>
<td>-3</td>
<td>-1</td>
<td>3</td>
<td>4</td>
<td>-3</td>
<td>0</td>
<td>4</td>
</tr>
<tr>
<td>2019-01-04</td>
<td align:?center?="">-2</td>
<td>-1</td>
<td>3</td>
<td>2</td>
<td>-5</td>
<td>-1</td>
<td>-2</td>
<td>4</td>
<td>2</td>
<td>3</td>
<td>-3</td>
<td>-2</td>
<td>3</td>
<td>4</td>
<td>-3</td>
<td>0</td>
<td>2</td>
</tr>
<tr>
<td>2019-01-03</td>
<td align:?center?="">-3</td>
<td>-1</td>
<td>3</td>
<td>3</td>
<td>-7</td>
<td>-1</td>
<td>-1</td>
<td>4</td>
<td>1</td>
<td>4</td>
<td>-4</td>
<td>0</td>
<td>3</td>
<td>4</td>
<td>-3</td>
<td>0</td>
<td>2</td>
</tr>
<tr>
<td>2018-12-30</td>
<td align:?center?="">-3</td>
<td>1</td>
<td>4</td>
<td>3</td>
<td>-7</td>
<td>-1</td>
<td>-1</td>
<td>4</td>
<td>0</td>
<td>4</td>
<td>-4</td>
<td>1</td>
<td>2</td>
<td>4</td>
<td>-3</td>
<td>0</td>
<td>4</td>
</tr>
</table>
</font>
</body>
</html>
```

Pelin ylläpitäjille lähetetään sähköpostilla pelin runkosrajan

```html
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=us-ascii"></head>
<body>
<style>
table, th, td {
border: 1px solid black;
border-collapse: collapse;
}
th {
text-align: left;
}
</style>
<font face="Arial"><h3>TESTIPELIN RUNKOSARJA 2019-01-12</h3>
<table style="width:50%">
<tr align="left">
<th>SIJOITUS</th>
<th>PELAAJA</th>
<th>PISTEET</th>
<th>PISTE MUUTOS</th>
</tr>
<tr>
<td>1.</td>
<td>PELAAJA 1</td>
<td>8</td>
<td>&#43;0</td>
</tr>
<tr>
<td>2.</td>
<td>PELAAJA 3</td>
<td>2</td>
<td>-4</td>
</tr>
<tr>
<td>3.</td>
<td>PELAAJA 2</td>
<td>-3</td>
<td>-2</td>
</tr>
<tr>
<td>3.</td>
<td>PELAAJA 4</td>
<td>-3</td>
<td>-4</td>
</tr>
<tr>
<td>5.</td>
<td>PELAAJA 5</td>
<td>-5</td>
<td>-4</td>
</tr>
</table>
<p> </p>
</font>
</body>
</html>
```