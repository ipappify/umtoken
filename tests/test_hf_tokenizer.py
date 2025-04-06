from umtoken.hf import UnimorphTokenizer

def test_from_pretrained():
    file = "./assets/ipt_eu3_24k_l3--tied.json"
    tokenizer = UnimorphTokenizer.from_pretrained(file, force_slow=True)

def test_encode_decode():
    file = "./assets/ipt_eu3_24k_l3--tied.json"
    tokenizer = UnimorphTokenizer.from_pretrained(file, force_slow=True)
    expected = "Hello, my dog is cute."
    ids = tokenizer.encode(expected, add_special_tokens=False)
    assert len(ids) >= 7
    actual = tokenizer.decode(ids)
    assert actual == expected

def test_batch_encode_decode():
    file = "./assets/ipt_eu3_24k_l3--tied.json"
    tokenizer = UnimorphTokenizer.from_pretrained(file, force_slow=True)
    expected = ["Hello, my dog is cute.", "I like to run."]
    enc = tokenizer.batch_encode_plus(expected, add_special_tokens=False)
    assert len(enc["input_ids"]) == 2
    actual = tokenizer.batch_decode(enc["input_ids"])
    assert actual == expected

def test_batch_encode_decode_pad():
    file = "./assets/ipt_eu3_24k_l3--tied.json"
    tokenizer = UnimorphTokenizer.from_pretrained(file, force_slow=True)
    expected = ["Hello, my dog is cute.", "I like to run."]
    enc = tokenizer.batch_encode_plus(expected, padding=True)
    assert len(enc["input_ids"]) == 2
    assert len(enc["input_ids"][0]) == len(enc["input_ids"][1])
    actual = tokenizer.batch_decode(enc["input_ids"], skip_special_tokens=True)
    assert actual == expected

def test_batch_encode_decode_truncate():
    file = "./assets/ipt_eu3_24k_l3--tied.json"
    tokenizer = UnimorphTokenizer.from_pretrained(file, force_slow=True, model_max_length=6)
    expected = ["Hello, my dog is cute.", "I like to run."]
    enc = tokenizer.batch_encode_plus(expected, padding=False, truncation=True)
    assert len(enc["input_ids"]) == 2
    assert len(enc["input_ids"][0]) <= 6
    assert len(enc["input_ids"][1]) <= 6
    actual = tokenizer.batch_decode(enc["input_ids"], skip_special_tokens=True)
    assert all(a in e for a, e in zip(actual, expected))

def test_batch_encode_decode_truncate_and_pad():
    file = "./assets/ipt_eu3_24k_l3--tied.json"
    tokenizer = UnimorphTokenizer.from_pretrained(file, force_slow=True, model_max_length=6)
    expected = ["Hello, my dog is cute.", "I like to run."]
    enc = tokenizer.batch_encode_plus(expected, padding=True, truncation=True)
    assert len(enc["input_ids"]) == 2
    assert len(enc["input_ids"][0]) == 6
    assert len(enc["input_ids"][1]) == 6
    actual = tokenizer.batch_decode(enc["input_ids"], skip_special_tokens=True)
    assert all(a in e for a, e in zip(actual, expected))

def test_batch_encode_decode_special():
    file = "./assets/ipt_eu3_24k_l3--tied.json"
    tokenizer = UnimorphTokenizer.from_pretrained(file, force_slow=True)
    tokenizer.set_prefix("[SOT]")
    tokenizer.set_suffix("[EOT]")    
    expected = ["Hello, my dog is cute.", "I like to run."]
    enc = tokenizer.batch_encode_plus(expected, add_special_tokens=True)
    assert len(enc["input_ids"]) == 2
    assert enc["input_ids"][0][0] == tokenizer.tokenizer.model.vocab_lookup["[SOT]"]
    assert enc["input_ids"][0][-1] == tokenizer.tokenizer.model.vocab_lookup["[EOT]"]
    assert enc["input_ids"][1][0] == tokenizer.tokenizer.model.vocab_lookup["[SOT]"]
    assert enc["input_ids"][1][-1] == tokenizer.tokenizer.model.vocab_lookup["[EOT]"]
    actual = tokenizer.batch_decode(enc["input_ids"], skip_special_tokens=True)
    assert actual == expected