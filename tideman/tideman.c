#include <cs50.h>
#include <stdio.h>
#include <string.h>
// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
} pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }
        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i], name) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }

    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // TODO
    for (int k = candidate_count - 1; k > 0; k--)
    {
        for (int j = 0; j < k; j++)
        {
            preferences[ranks[j]][ranks[k]]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // TODO
    pair_count = 0;
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int k = i + 1; k < candidate_count; k++)
        {
            if (preferences[i][k] > preferences[k][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = k;
                pair_count++;
            }
            else if (preferences[k][i] > preferences[i][k])
            {
                pairs[pair_count].winner = k;
                pairs[pair_count].loser = i;
                pair_count++;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory

void sort_pairs(void)
{
    int margin[pair_count];

    for (int i = 0; i < pair_count; i++)
    {
        // visual of pairs array
        // printf("%i%i\n", pairs[i].winner, pairs[i].loser);
        // calc margin of victory
        margin[i] = preferences[pairs[i].winner][pairs[i].loser] - preferences[pairs[i].loser][pairs[i].winner];
        // printf("\n%i\n", margin[i]);
    }

    for (int k = 0; k < pair_count - 1; k++)
    {
        int marginlarger = margin[k];
        int maxindex = k;

        for (int j = k + 1; j < pair_count; j++)
        {
            if (marginlarger < margin[j])
            {
                marginlarger = margin[j];
                maxindex = j;
            }
        }

        int tempmargin = margin[maxindex];
        margin[maxindex] = margin[k];
        margin[k] = tempmargin;
        pair temp = pairs[maxindex];
        pairs[maxindex] = pairs[k];
        pairs[k] = temp;
    }

    for (int i = 0; i < pair_count; i++)
    {
        // printf("%i%i ", pairs[i].winner, pairs[i].loser);
    }
    // printf("\n");

    return;
}

bool cycle(int i, int k, int c)
{
    printf("%i\n", c);
    if (c == k)
    {
        return true;
    }
    for (int j = 0; j < candidate_count; j++)
    {
        if (locked[k][j] == true)
        {
            if (cycle(k, j, c))
            {
                return true;
            }
        }
    }
    return false;
}
// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{

    for (int i = 0; i < pair_count; i++)
    {
        int originalwinner = pairs[i].winner;
        int originalloser = pairs[i].loser;
        if (!cycle(pairs[i].winner, pairs[i].loser, pairs[i].winner))
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }

    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            // printf("%i", locked[i][j]);
        }
        // printf("\n");
    }
    return;
}
// Print the winner of the election
void print_winner(void)
{
    // TODO
    int winnerarray[candidate_count];
    for (int i = 0; i < candidate_count; i++)
    {
        winnerarray[i] = 0;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i])
            {
                winnerarray[i]++;
            }
        }
    }
    for (int i = 0; i < candidate_count; i++)
    {
        if (winnerarray[i] == 0)
        {
            printf("%s\n", candidates[i]);
        }
    }
}
