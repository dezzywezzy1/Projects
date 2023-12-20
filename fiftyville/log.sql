-- Keep a log of any SQL queries you execute as you solve the mystery.

/* SELECT * from crime_scene_reports
WHERE year = 2021
AND month = 7
AND day = 28; */

--Robbery happened at 10:15am

SELECT transcript
FROM interviews
WHERE year = 2021
AND month = 7
AND day = 28;

--theif took earliest flight out the next morning
--call with this person lasted less than a minute
--ATM on legget street, thief withdrew money the morning of
--within 10 minutes of theft, thief drove away

SELECT name, passport_number, license_plate
FROM people
WHERE id IN (
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN (
        SELECT account_number
        FROM atm_transactions
        WHERE month = 7
        AND day = 28
        AND year = 2021
        AND atm_location = "Leggett Street"
    )
AND phone_number IN (
    SELECT caller
    FROM phone_calls
    WHERE year = 2021
    AND month = 7
    AND day = 28
    and duration <= 60
)
);

SELECT id, hour, minute, origin_airport_id, destination_airport_id
FROM flights
WHERE day = 29
AND month = 7
AND year = 2021
AND origin_airport_id = (
    SELECT id
    FROM airports
    WHERE city LIKE "fiftyville"
)
ORDER BY hour ASC
LIMIT 1;
/* destination_id = 4, flight_id = 36 */

SELECT passport_number
FROM passengers
WHERE flight_id = 36
AND passport_number IN (
    SELECT passport_number
    FROM people
    WHERE id IN (
        SELECT person_id
        FROM bank_accounts
        WHERE account_number IN (
            SELECT account_number
            FROM atm_transactions
            WHERE month = 7
            AND day = 28
            AND year = 2021
            AND atm_location = "Leggett Street"
        )
    AND phone_number IN (
        SELECT caller
        FROM phone_calls
        WHERE year = 2021
        AND month = 7
        AND day = 28
        and duration <= 60
        )
    AND license_plate IN (
        SELECT license_plate
        FROM bakery_security_logs
        WHERE day = 28
        AND month = 7
        AND year = 2021
        AND hour = 10
        AND minute BETWEEN 15 AND 30
        )
    )
);

/* passport_number = 5773159633
    name = bruce
    license_plate = 94KL13X */

SELECT full_name, city
FROM airports
WHERE id = 4;

SELECT *
FROM people
WHERE name = "Bruce"
AND passport_number = 5773159633
AND license_plate = "94KL13X";

SELECT *
FROM people
WHERE phone_number = (
    SELECT receiver
    FROM phone_calls
    WHERE caller = (
        SELECT phone_number
        FROM people
        WHERE name = "Bruce"
        AND passport_number = 5773159633
        AND license_plate = "94KL13X"
    )
    AND day = 28
    AND month = 7
    AND year = 2021
    AND duration <= 60
);


/* Bruce stole the duck and flew to NYC with the help of his accomplice Robin */ 