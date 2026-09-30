---
title: "Whose Bias Are We Building?"
description: "AI safety rules also distribute capability and power. More intelligent systems still need a defensible account of whose judgments govern everyone else."
date: 2026-09-29
tags: [ai-governance, alignment, ai-safety]
image:
  path: /assets/images/notes/whose-bias-are-we-building.jpg
  alt: "Three differently cut keys shaping a city of buildings and connected streets"
---

Imagine an AI company's CEO becomes convinced that eating animals is wrong. The company's general-purpose assistant starts refusing to order chicken. You wanted groceries. You got an ethics seminar with an empty shopping cart.

The CEO might have serious reasons: animal suffering, environmental costs, a coherent moral position. A vegan shopping service would be straightforward. Its purpose is part of the deal. The harder case is an assistant people already depend on, whose owner introduces a rule governing what everyone else may buy through it. A conviction can deserve consideration without automatically deserving authority over someone else's dinner.

This is a thought experiment. It is also a small version of a much larger question: whose judgments become constraints when AI mediates more of what we do?

![Three differently cut keys shaping a city of buildings and connected streets](/assets/images/notes/whose-bias-are-we-building.jpg)

## A safety boundary is also an access boundary

Cybersecurity makes the question harder. A capable assistant that helps a defender find a vulnerability may help an attacker find one too. Restricting that capability can protect people. It can also prevent a legitimate defender from doing useful work.

“It's my system” cannot settle the matter. Attackers can say that too. Verification, the nature of the assistance, and the consequences of misuse all matter. Grocery shopping and cyber attacks are different moral cases. The shared question is who has authority to draw a boundary, and who gets through it.

That allocation is already concrete. In September, OpenAI announced that it would offer Ukraine's government its Daybreak program for civilian infrastructure defense, including authorized vulnerability review and fixes. This is an access commitment, not proof of improved security or evidence that other defenders are excluded. But it shows the mechanism: valuable capability can be distributed through institutional relationships.[^daybreak]

It helps to separate questions that “bias” often bundles together. Inventing a vulnerability is a factual error. Systematically giving some interests more weight is a directional slant that may warrant scrutiny. A refusal might express a preference, implement a legal obligation, or enforce a defensible safety constraint. The refusal alone doesn't tell us which.

Nor does a good safety rationale erase the distributional effect. A well-designed boundary can still advantage institutions able to demonstrate trustworthiness over people without the resources or connections to do so. That possibility doesn't establish unfairness. It makes access, evidence, and appeal part of the safety question.

## Who gets to write the rule?

The major labs aren't hiding the fact that their systems have governing principles. Claude's constitution describes intended ethical priorities, acknowledges that Anthropic can be mistaken, and asks Claude to challenge unethical requests even from the company itself. OpenAI's Model Spec balances empowering users and developers, preventing serious harm, and protecting the company from legal and reputational harm. It also establishes which instructions prevail when interests conflict.[^constitution][^spec]

Those are consequential design choices. A general assistant serves the user within a framework that also reflects its provider's responsibilities and interests. Publishing that framework makes scrutiny possible. It doesn't demonstrate that deployed models always follow it, or that every rule deserves the authority it claims.

Government adds a different lever. The Trump administration's order on ideological neutrality makes its definition a condition of federal purchasing. The order invokes truth-seeking while identifying DEI as ideological dogma, and allows certain disclosed or user-requested ideological judgments. Its scope is federal procurement, not all private AI use.[^order]

The implementation gives those words commercial teeth. Relevant terms can affect eligibility, payment, and termination, alongside requirements for documentation and user feedback. A government's interpretation of acceptable bias can therefore help determine who gets a contract.[^omb]

Truth-seeking is a defensible aspiration. The disputed part is which judgments count as neutral, how that is tested, and whether the standard treats competing positions consistently. An executive order can authorize purchasing rules. It cannot, by declaration, prove a model unbiased.

The easy story would cast founders as wanting unchecked control and government as the corrective. The current positions are more interesting. Dario Amodei argues for binding regulation, third-party testing, and checks on both corporate and state power. He proposes access to AI advice comparable to the state's when people challenge adverse government action. Capability can counter concentrated power as well as reinforce it.[^amodei]

OpenAI likewise calls for mandatory safety rules and independent assessment.[^window] These commitments matter. The unresolved issue survives them: an external regulator or assessor still needs a remit, standards, appointments, and a way to challenge its decisions. Technical expertise supports a claim to be heard. Holding public office supports a claim to act. Neither settles the merits of every rule.

Access and procurement are economic mechanisms, not merely philosophical disagreements. Qualifying for a capability or contract can confer a productive advantage. Their actual effect depends on alternatives, the capability involved, and who can meet them. As organizations build workflows around a provider, changing its rules can also become harder to absorb. A preference that once shaped a single answer can become a condition of participation: which research receives assistance, which tools developers can build, which work a public agency can buy. That is how a judgment can become infrastructure.

Users aren't the only people with a stake. Someone exposed to an AI-assisted cyber attack may never have used the assistant. Imagine a deployment that improves useful services while adding substantial electricity or water demands to its host community. Residents cannot avoid that tradeoff by switching chatbot subscriptions. A company-customer contract is too small a framework for consequences that reach outside it.

## A smarter successor doesn't inherit a mandate

AI is also becoming involved in the work of improving AI. Anthropic's original Constitutional AI method used human-authored principles to guide model-generated critiques, revisions, and comparisons. That is a documented training method, not a complete account of current Claude training.[^cai]

Such feedback can be useful. A model can expose an inconsistency, generate a counterargument, or help test whether a safeguard prevents a real failure. Empirical evidence doesn't become worthless because an evaluator shares the designer's values. But agreement with a principle is not independent proof that the principle deserves to govern others.

Recursive self-improvement would extend the loop: AI contributes improvements that produce a more capable successor, which contributes further improvements. OpenAI says fully autonomous recursive self-improvement isn't happening today, while describing current research assistance and ambitions for human-supervised automated researchers.[^window] That distinction matters. Assistance is happening; an autonomous improvement spiral remains hypothetical.

If successors become more involved in designing later systems, their objectives and evaluation rules become more consequential. Inherited values need not remain fixed, and another model isn't automatically an independent judge. Better reasoning may reveal better policies. It doesn't confer permission to impose them.

The useful question isn't whether we can remove every value judgment from AI. We can't specify what it should do without making some. It's whether a particular boundary has evidence proportionate to its restriction, whether mistakes can be challenged in practice, and whether materially affected outsiders have a voice.

Evidence of abuse can justify tighter access. Repeated denial to verified legitimate users can justify revising a boundary. Costs imposed on people outside the transaction can require a broader decision process. These are reasons to change a rule, not branding exercises or a demand that everyone receive a veto.

“Our model agrees with us” tells us little without knowing what was tested. Even demonstrated compliance would leave a separate question: why should this rule govern other people? A defensible account of alignment must explain why the rule deserves authority and who can contest it. More intelligent AI can help us examine that account. Intelligence alone cannot supply the mandate.

[^daybreak]: [OpenAI's announcement of Daybreak access for civilian defense in Ukraine](https://openai.com/index/openai-extends-cyber-access-to-ukraine-for-civilian-defense/).
[^constitution]: [Claude's January 2026 constitution, pinned source](https://github.com/anthropics/claude-constitution/blob/84fa9a2711837780ffdddf9d9f32820c92f92ede/20260120-constitution.md).
[^spec]: [OpenAI Model Spec, August 18, 2026](https://model-spec.openai.com/2026-08-18.html).
[^order]: [Executive Order 14319, Preventing Woke AI in the Federal Government](https://www.whitehouse.gov/presidential-actions/2025/07/preventing-woke-ai-in-the-federal-government/).
[^omb]: [OMB's implementation memorandum, M-26-04](https://www.whitehouse.gov/wp-content/uploads/2025/12/M-26-04-Increasing-Public-Trust-in-Artificial-Intelligence-Through-Unbiased-AI-Principles-1.pdf).
[^amodei]: [Dario Amodei's June 2026 policy essay](https://darioamodei.com/post/policy-on-the-ai-exponential).
[^window]: [OpenAI on the AI policy window, September 9, 2026](https://openai.com/index/ai-policy-window/).
[^cai]: [The original Constitutional AI paper](https://arxiv.org/abs/2212.08073).
