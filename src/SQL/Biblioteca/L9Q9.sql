SELECT
    l.titulo
FROM
   Livro l
LEFT JOIN
    Reserva r ON r.id_livro = l.id_livro
WHERE
    r.id_livro IS NULL;
    
