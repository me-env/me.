
DROP TABLE IF EXISTS me_banking.transactions;

CREATE TABLE IF NOT EXISTS me_banking.transactions (
    id                  SERIAL PRIMARY KEY,
    transaction_id      text NOT NULL,
    transaction_name    text NOT NULL,
    account_id          text NOT NULL,
    account_name        text NOT NULL,
    amount              float4 NOT NULL,
    type                text[] NOT NULL,
    tx_date             timestamp without time zone NOT NULL,
    timestamp           timestamp without time zone DEFAULT now() NOT NULL,
    refunded            bool DEFAULT False NOT NULL,
    double_checked      bool DEFAULT False NOT NULL,
    payment             bool NOT NULL,
    unique(transaction_id, account_id)
);

-- Example
INSERT into me_banking.transactions
            (transaction_id, transaction_name, account_id, account_name,
            amount, type, tx_date, refunded, double_checked, payment) VALUES
            ('0001', 'test', '00001', 'acc_test', 1.5, '{"type1", "type2"}', '1996-12-02 04:05:06', True, False, True);


INSERT into me_banking.transactions
            (transaction_id, transaction_name, account_id, account_name,
            amount, type, tx_date, refunded, double_checked, payment) VALUES
            ('6ee84b38e0744e06a80b28a09128b291', 'test', 'de0074746603468b9259d368e13e6fa3', 'acc_test', 1.5, '{"type1", "type2"}', '1996-12-02 04:05:06', True, False, True) ON CONFLICT (transaction_id, account_id) DO NOTHING;


select * from information_schema.columns where table_schema = 'me_banking' AND table_name = 'transactions' ORDER BY ordinal_position;




