select person.firstName, 
person.lastName,
address.city,
address.state
from person as person
left join address as address
on person.personID = address.personID