# my new reality of software engineering

## Raw Notes

# intro [editorial note, I dont want this to be the section heading, it needs to be something else]

I have been a software engineer for more than twenty years. Looking back, its amazing how many things have changed in that time, and how many things haven't. But what has happened in the last year, (especially the last 6 months) has created a fundamental shift in how I work, how I think, how much I produce, and really what it even means to be a software engineer.

I was lucky (I think) to have always known that I wanted to write software as a career. I knew I wanted to work with computers from the moment I heard about them, before I ever actually touched one. When I was around 6 my parents got me a VTech PreComputer 1000 [editorial note: Id like to insert a picture of one into the article below the paragraph that mentions it, and link to the wikipedia article for it.], a simple device that had math and geography quizes, a very non-standard terrible keyboard and a single 20 charachter dot matrix lcd display. But it had a mode where you could write BASIC and came with a spiral notebook that gave you a little information about how it worked. Writing line numbers when you could only see a single line at a time was quite the challenge, but I spent hours writing programs in that thing. Worse yet, it didnt have any non-volitle storage, so if you turned the power off, your program was gone. That didn't stop me from writing the programs over and over again, debugging and playing with it for hours at a time. I made computer monitors, cases, keyboards, out of cardboard boxes and markers, just to pretend.

The idea that I could make this thing do things was so empowering and enchanting for me. Like actual magic spells that brought my whims to reality. And there was always this entertwined tension between wanting to learn the languages, the patterns and better, more efficient ways to write the code, and the actual production of the thing I was trying to build. Both brought me so much joy.

And its been that way for my entire career. I've loved the actual writing of the code, the sound of my hands on the keyboard, the diffs in version control, but more importantly the problem solving challenge and the problems I was solving for my users and customers. I was making lives easier, bringing joy to other people, or making them (and me) money. But it always required me to do all of the work: understanding the problem or challenge or pain point, coming up with a solution, making that solution a reality, debugging the existing code, building, testing, iterating, showing it to other people, and getting it into production.

And now we have these LLMs that can help. I was at my current job (its only been a few years, but it seems like so long ago) when chatgpt was first released. It was such a novelty at first, then we started getting scared that our jobs were over. Then we settled into the reality that while these things were cool, they had major limitations, the hallucinated, they couldn't keep much information in context, there was no way they were going to be able to handle our hundred-thousand-line codebases. We were thinking about when their knowlege cutoffs were, figuring out how they might be useful, and some of us were imagining a future where they could do so much more, but that wasn't reality and wasn't near term.

And slowly but surely things improved. We got new models, we got new tools that could use them. When I started at my current job we had lots of challenges where we needed to do something but we needed to do it at a scale that would mean hiring dozens if not hundreds of people if we wanted to do it fully and repeatedly. There was no way we could hire that many people much less manage them. But we started building towards that future anyway, thinking that one day this might be possible.

Then claude code came out. We started playing with it and it was great, but a very different way of working. Sonnet 3 came out, and it was too expensive to spend too much time in, but we used it more and more. More new models came out, we gave it a little more to do, but still I was writing the majority of the code, just using it for some parts that were obvious and routine.

Then middle of the year last year sonnet 4 came out. The conversation started to change, people started saying it could do so much more. I decided to start using it a lot more, letting it write the code like 75% of the time. I was still using things like cursor tab completion and writing large blocks of code myself, but I slowly gave it more and more. I was working on large scale systems, some from scratch, some existing. Large, ambitious projects, the kinds of things I love and really am known for. Architecture level things. And it was handling it all. It could answer my questions, give me ideas, challenge my plans, and then execute on it.

And then. In the last month Opus 4.6 and then Codex 5.3 came out. My CTO put out a memo to everyone that we shouldn't be writing most of the code anymore, we should be using the agents. They're smart enough, fast enough, thorough enough. Good enough. I had already decided to try and go all in - I was a little relieved when the memo came out, I was a little worried that someone was going to be coming to me soon about how much money I was spending!

And so now I haven't written more than a dozen lines of code by hand in the last month. Codex writes my code, helps me plan, manages git, creates my commits, pushes my pr, responds to review comments and addresses them, manages my stories, just about everything. I'm shipping more than ever, getting more done than ever, but writing virtually no code to do it. I'm talking to an agent like I would talk to a collegue in slack. I'm writing in languages that I am not nearly as fluent in. It doesn't matter, im still writing quality code, that does the job as well as if written by an expert in those languages. It's a whole new world.

# The new reality

In some ways, this world has changed so fast, and in others it happened slow enough that you could start thinking and planning for it if you were paying enough attention. I told someone a year ago that before long it will be like we are all engineering managers with full teams of employees. That is really the way I feel now.

But this reality is not evenly distributed. At my job, in my twitter, we are in a bubble. We are in many ways on the bleeding edge, consuming this like a firehose, jumping from tool to tool and model to model and trying our hardest to learn the new meta as soon as it comes out, and we can't keep up. We are pushing it as far as it will go, and there is still lots of gaps and holes, but we can see a future coming where those problems will be solved. But of course the majority software engineers in the world are still working like they did last year and the twenty years before, most of them very happy to keep doing things that way. I'm partially writing this to tell them that they have to confront this new reality because it's coming for them whether they like it or not. You might be able to last another 6 months, or a year. In some niche pockets maybe longer. But five years from now the software engineering landscape will look completely different. Expectations of how and what you can produce will completely change.

Whenever I interview for my next job, right after we talk about compensation and benefits, one of my biggest questions will be my inference budget and flexability of agent tooling. More importantly, I expect that my familiarity and success with agents will be a major part of their questions and expectations for me.

But there will be many new problems, mostly social and "around" the software engineering process that we will have to figure out. Things that were the bottlenecks before won't be, and new bottlenecks will be crop up.

[todo: need more here about the new challenges we will face in the new paradigms]

[theres a thing I would like to say about how the things we have done as software engineers hasnt really changed in twenty years. New tech, new frameworks, new languages have come that we've had to learn, but fundamentally the things you had to do and the way you had to work has stayed the same. The shift now is revolutionary, a complete phase shift of how we do the job. I dont know where this belongs or really how to say it.]

# my suggestions for how to get started and how to think about using agents as software devs

[this is a transcript of a conversation I had with some people earlier, I want to extract the ideas out of this and write prose about it. RyanGuill is me, treat the messages from everyone else as context, we will not include their words or their names at all.]

```
10:20]hipx
: ahhh gotcha. this is the first time I’ve leaned into the plan mode 100% and then agent. was super helpful to have the fat markdown file it made before actually doing anything so I could read through its plan, make changes, etc
[10:39]RyanGuill: yeah, plan mode is great, essential really when youre doing anything even moderate in size. Using a plan mode, and telling it "ask any questions if you have them" makes a huge difference. in fact you can go further and say something like "ask me questions relentlessly about every part of this plan until there is no ambiguity or problems." and even "use a subagent with no context to review the plan and ask questions, identify gaps or problems, or make recommendations"
[10:52]hipx
: oooo that’s smart
[10:54]RyanGuill: I put the ask questions at the end of almost every prompt
[10:55]RyanGuill: at this point I use codec to make a branch, merge main, make commits, push, make a detailed pr, even reply to and resolve review comments
[10:56]Ekzos: that is wild
[10:56]Ekzos: love the "ask questions" and "use subagent with no context"
[10:57]Ekzos: maybe I'll get there eventually, but I have to be honest, I still feel uncomfortable asking an AI to interact with other systems for me
[10:57]RyanGuill: I really believe the future is we are all engineering managers with agents as our engineers
[10:57]Ekzos: like, it doesn't bother me at all to ask for a response or ask for changes in my editor, maybe just because of the proximity
[10:59]Ekzos: lol, more like engineering middle-managers 😂
[10:59]RyanGuill: yeah, takes time to get comfortable and build that trust. you do have to learn the edges of what its capable of and where it might get confused or do something wrong, but just take it slow and push out of your comfort zone a little every day. but the things it cant do gets smaller all the time
[10:59]Ekzos: that is a super interesting thing I hadn't really considered until you put it that way though. you're probably right
[10:59]RyanGuill: but once you get there, you can do way more things at once.
[11:00]RyanGuill: our biggest problem right now for all the engineers at work is how to run multiple instances of the stack at once so you can do more things
[11:01]Ekzos: that's great advice, and that does address some of my feelings on it, but I also worry about hallucinations during/before/after those interactions. I'm not sure how that's fully solved, maybe it can be though. I know hallucinations have gotten way less prevalent already, so maybe it's an unrealistic worry
[11:02]RyanGuill: I havent had anything I would consider a hallucination in months
[11:02]RyanGuill: I have had it get something wrong, but its almost always that I wasnt clear or specific enough
[11:02]Ekzos: "run multiple instances" lmao, that's wild
[11:04]RyanGuill: think about all the times you think about something youd like to do but its not what youre currently doing or should be its own pr or just the work to make a branch, write tests, build a pr, all the other stuff around the change makes it not worth it.  but if it can cook those things somewhere else with just a little instruction while youre on the main quest you just lowered the “activation energy” a ton
[11:05]Ekzos: no argument there at all
[11:05]RyanGuill: burn down the tech debt
[11:05]RyanGuill: my other biggest challenge is finding people to review all my prs
[11:09]Ekzos: yeah, I'm sure that it depends on the models you use and how good you get at interacting with them, but I frequently get annoyed at cursor for giving me bad suggestions. things that are very obviously not what I would want to do, referencing APIs that don't exist, etc.

but I just leave it on 'auto' and mostly use tab suggestions, so it's a different thing that what you're talking about. I do think that my experience has been better (less of those annoyances) when I use cursor's "ask"/"agent" modes.
[11:10]Ekzos: I guess my experience just hasn't been as impressive, but that's not to diminish yours at all, I'm really glad to hear it's going well
[11:13]Ekzos: (back to having it interact with other systems for me) I think there's just something in me that wants to be "the one to push the button" if that makes sense.

I know it's kinda arbitrary where we draw that line, and it's a continually moving thing as technology changes, but still my monkey brain pushes back a little lol
[11:13]RyanGuill: heres what I would tell you to do:
get an openai subscription
get opencode desktop
use codex-5.3
write a good agents.md that specifies the things that are important, tell it how to find things in the code base, how to build/lint/run tests. anytime you see the agent go in a wrong direction, add something to the md file to help it know how to do it right. you can use llm to write it for you, interview you about things to add
then stay out of your ide entirely and interact with the llm only. no matter how small the change is. you can see the diffs right there.
[11:14]RyanGuill: just try it for a few tasks, start small, see how it goes
[11:15]RyanGuill: cursor is a crutch at this point, itll hold you back
[11:15]RyanGuill: (traveling, back in a bit)
[11:24]Ekzos: yeah, again, good advice, and probably advice I should take. the problem is it requires me to stop doing the thing I like doing. or at least, that's how it seems to me.

maybe the thing I like doing will still be there on the other side, but it feels like I won't get to do the creative/inventive part of my job anymore (which is what I like the most) give me a good problem to solve and let me go solve it, I don't want to farm it out to someone else, b/c then I don't get the satisfaction of solving it... right?

maybe having done this for a bit and being 'on the other side' of it you might say that you get that satisfaction in a different way.

(to be clear, by 'on the other side' I just mean fully leaning into AI vs only dabbling like I have)
[11:31]RyanGuill: yeah for real, we talk about this a lot. if you enjoy the code itself, this sucks. but id argue if you enjoy solving problems, youre still doing that. but really at this point you have to love shipping more than coding
[11:32]RyanGuill: solving problems
[11:36]Ekzos: yeah, that's fair. you're still solving the problem, just in a different way. I do think there's something different about your brain being the one that does the work, like mechanically in your brain I mean. But if I'm honest, how many truly complex problems am I solving on a daily basis? not very many at all... most of what I'm doing is pattern matching or basic research which is what AI is really good at lol
[12:04]RyanGuill: you know me, I love thinking about the micro optimizations and the algorithms, but you still get to do that when it matters, youre just outsourcing the bookkeeping and typing. I miss the code, but I like the productivity more.
[12:05]RyanGuill: but also youre still in control of the solution and the code, but think of the llm as a partner. collaboration, constructive criticism, challenging. I think in coming up with better solutions because its thinking through my thinking and probing the edges of it
```

[I dont know how to fit this in or where it goes, probably needs a lot of rewording]
In some ways this feels a bit like when source control was a new thing. When subversion started to become mainstream (yes I am that old) I remember having debates and having to proselytize why it was a good, necessary way of working, worth learning and adopting. There were many people who resisted at first. subversion itself wasn't particularly easy to work with (I know git seems hard sometimes now, but its considerably easier than it was!). Even some people who were struggling with the things it solved were sometimes reticent to learn it. We take it for granted today, but back then making a copy of your code before a change was just the way we worked before. But of course this is much bigger. After version control you still did the same things you did before, just maybe had more steps or did things in a different way. Nothing fundamentally about the job, just a bit of your process. This new way of working is much more revolutionary.

"Revolutionary" strikes me as a really interesting and apt word here. A lot of times we use "revolutionary" in completely positive connetations in tech. Who doesnt want a revolutionary new product? But actual revolutions are messy, ugly, sometimes violent. There are winners and losers. There are people very happy with the status quo, who will resist as long as they are able. In this revolution there wont be good guys and bad guys, people who are right and who are wrong, this isnt and shouldnt be a holy war. But I do believe it is an inevitablity. I might be wrong about the timeline, but I don't think im wrong about the reality of our future. I'm afraid we need to start mentally preparing ourselves for what comes next. The economics alone will force the shift.



If you are a software engineer because you like typing on the keyboard, writing the actual code, thinking about the control flow of the program through each successive line in the file, this _sucks_. It does. I certainly think I am one of those people. I think I have softened my attachment to the actual code over the last decade of working in startups, but I have always cared deeply about not just the outcome but also the formatting, organization, elegance, and clarity of the code I produced. I tried to leave the code better than the way I found it with every PR. I cared deeply about the names of variables, had debates about comments in code, fought in the tabs vs spaces wars. I had opinions on the esthetics of the files. I am not happy about leaving that behind. I worry that my ability to read and write code will languish over time, and that somehow that will affect my ability to reason about the software itself.

but. If you care about solving problems, and shipping, this might be the best thing thats ever happened. In so many jobs in my career I was an advocate for our tech-debt column in the project management system. There were so many things that we would _want_ to do, but couldnt find the time for. There was never enough time, never enough people to get everything done. We needed to ship that new feature, fix that priority bug, and do the next thing. Going back to maintain that old code, or make that improvement was things you only got to do if you were lucky or snuck it in. We can do those things now. Most of the time those things were not difficult, they didn't need a genious to implement, they required _time_. Time you did have. But now, you can give your wisdom and desires to an agent who can do those things for you, and all of the bookkeeping around it that made it so much harder. How many times have you looked at what would be a change of only a few lines but chose not to do it because those few lines were hours of work when you considered making the story, creating the branch, writing the tests, creating the PR, asking for reviews, iterating on the review comments, and deploying it. Now those things are so much easier. In my day to day I have a main quest or two, and may have a handfull if not a dozen side quests that I'm also tackling at the same time. These new capabilities lower the "activation energy" of getting things done tremendously. Which is good for you, and good for your customers.

Because at the end of the day, we are paid to ship. The shipping has to be the goal. It's been great for the past twenty years that I've been paid to do this thing I love _because_ I was shipping value to customers, but it was the value that I was paid for, not the symbols I wrote. I will mourn the loss of the artisinal hand-written code.

When I am really honest with myself though, I am happiest when I am "productive". Thats such a hard word to define, almost an emotion. But when I go to bed at night, I feel the best when I feel successful at getting something new out into the world, a desire made into reality. The mechanics of doing that I have always found pleasure in, but that was never the thing that mattered, what matters is shipping.




[section: my suggestions on how to get started]

If you are curious but still uncomfortable, I think the answer is not "go all in tomorrow" and not "ignore this for a year." Start small with low-risk tasks where the blast radius is tiny and you know exactly the change to be made. Ask the agent to do it instead, like you would if you were telling a coworker how to do it. Review the diff. Run tests. See what it got right, what it missed, and where your instructions were vague. Then do it again.

The biggest unlock for me was moving from "ask mode" to explicit planning. Before any moderate change, have the agent produce a plan first. Then force it to ask clarifying questions until there is no ambiguity. I often tell it to be relentless about questions, assumptions, and edge cases. You can go one step further and ask a second agent, with no context, to review the plan and challenge it.

I am a big proponent of "writing is thinking". How many times have you jumped into code before you had a solid plan and then realized that you forgot a piece, or run into a challenge that you really should have thought of beforehand. You learned that there was a size and complexity of problems that you needed to write out your plan first so you could think it through holistically, and maybe let other teammates review and give you feedback. Maybe you wrote a PRD or scope. This is really an extension of those concepts, except now you can have the agent collaborate with you on it.

As you start you'll find that theres certain things you have to say or remind the agent to do, things that you just inherently know to do but you have to spell it out for the agent. Thats where the `AGENTS.md` / `CLAUDE.md` file comes in. Put your conventions, architecture constraints, testing commands, lint/build workflow, and gotchas in one place. Treat it like living documentation for how work gets done. Every time the agent goes wrong in a repeatable way, update the file so it is less likely to make the same mistake again. Have the agent help you write it. Have it explore your codebase and make a map for itself.

Trust builds from repetition, not from one impressive demo. At first, keep your hand on the wheel for anything that touches external systems: deploys, migrations, production settings, billing surfaces. Over time, as results become predictable, you can delegate more of the full loop: branch setup, implementation, tests, commits, PR creation, review response, and cleanup. The goal is not blind trust. The goal is reliable delegation with verification.

You still must review the code! You can still be opinionated about how the code is written, formatted, organized. As much as you can codify those things in your `AGENTS.md` but keep iterating with the agent. Let it do something, review it, give it feedback. Tell it to refactor, tell it you don't like that variable name, tell it when it forgot a step (or you did). You are still responsible for the code you're shipping, even though you aren't the primary author anymore.

This is the mindshift: judge this workflow by shipping outcomes, not by how much code you personally typed. I still care about code quality and design choices, but I spend less energy on the bookkeeping around changes. That lowers the activation energy for all the little improvements we used to postpone forever. Tech debt gets burned down. Side quests that never seemed worth the overhead actually get done.

You do not have to stop being an engineer to use this model. You still own the problem framing, architecture decisions, constraints, and quality bar. You are still accountable for what ships. The difference is that execution becomes collaborative and parallel. In practice, that means you can do more at once, if your team can absorb the review load and process throughput that comes with it.

So my practical recommendation is simple: start small, be explicit, require plans and questions, document your rules, and gradually expand delegation. You will find your own edge of comfort. Then push it a little farther each week.

## Theme Buckets (Iteration 1)

1. A long-stable profession, then a phase shift
   - The job changed tools and frameworks for 20 years, but not the core workflow.
   - The last year changed the workflow itself: from "I do every step" to "I direct an agent system."
   - This is the core argument and should be stated clearly early.

2. Personal origin story and identity tension
   - Childhood computing story (VTech PreComputer 1000) as emotional anchor.
   - Lifelong love of code as craft (typing, diffs, algorithms) vs love of solving problems and shipping.
   - Emotional truth: this transition is productive but comes with loss for people who love writing code directly.

3. Adoption timeline (novelty -> skepticism -> partial use -> all-in)
   - ChatGPT novelty and fear.
   - Early practical limits (hallucinations, context limits, weak repo handling).
   - Claude/Codex progression and trust curve.
   - Current state: agent-first workflow, minimal hand-written code, high output.

4. New operating model: software engineer as director
   - "Engineering manager of agents" framing.
   - Work shifts toward planning, constraints, review, QA, and orchestration.
   - Inference budget + tooling flexibility become top job-quality criteria.

5. Uneven distribution and near-future pressure
   - Early-adopter bubble vs broader industry lag.
   - Claim: most engineers will be forced to adapt in short order.
   - Keep this firm but grounded (avoid overclaiming certainty).

6. New bottlenecks and organizational constraints
   - Review bandwidth, stack concurrency, process throughput, social trust.
   - Not "can model write code?" but "can team absorb and validate output?"

7. Practical adoption guidance
   - Start small, build trust gradually, expand scope.
   - Use plan mode, force clarifying questions, use independent review subagents.
   - Codify project constraints in AGENTS.md and update it based on mistakes.

## Candidate Section Structure (For Rough Draft Only)

1. Working title and framing hook
   - Replace current "intro" heading with a stronger section name.
   - Candidate section names:
     - "A Career That Suddenly Changed"
     - "Twenty Years, Then a Phase Shift"
     - "When the Job Itself Changed"

2. Why this hits me personally
   - Childhood origin story + craft identity.
   - Add image callout under VTech paragraph.
   - Link target: https://en.wikipedia.org/wiki/VTech_PreComputer_1000

3. What changed (timeline)
   - Condense tool/model chronology into a tight "then -> now" progression.
   - Emphasize behavior change, not release-note history.

4. What my work looks like now
   - Concrete list of delegated tasks (planning, coding, git, PRs, review responses).
   - Keep one grounded mini-example of a recent task flow.

5. The uncomfortable tradeoff
   - "If you love code itself, this can feel bad."
   - "If you love shipping and problem-solving, this can feel incredible."
   - This likely becomes the emotional center of the post.

6. Why this matters for other engineers
   - Uneven distribution now, convergence later.
   - Explain what changes in hiring/interview expectations.

7. How to get started without going all-in on day one
   - Pull distilled guidance from transcript into concise prose.
   - Give a staged adoption path (small tasks -> larger tasks -> system interactions).

8. What gets harder next
   - New bottlenecks: review load, process design, trust and verification, multi-agent coordination.
   - End with pragmatic call to experiment now.

## Transcript Extraction Notes (Ideas to Reuse)

- Planning quality is leverage: use plan mode and require aggressive clarifying questions.
- Add independent critique: ask a no-context subagent to challenge plan gaps.
- Keep a living AGENTS.md as operating manual; update it whenever the agent fails.
- Trust grows with exposure: start with low-risk tasks and expand scope.
- The "activation energy" for side improvements drops when agents can run parallel streams.
- Throughput shifts bottlenecks to PR review and environment orchestration.
- Hallucination concern is now more often a specification-quality problem than random fabrication.
- Core mindset shift: from typing/code production to orchestration/decision ownership.

## Questions for Agent

- Where should the strongest thesis sentence appear: opening paragraph or end of first section?
- How hard should the "you must adapt" claim be pushed to stay persuasive without sounding absolutist?
- Should the post include one concrete anonymized work example to ground productivity claims?

## Non-Negotiables

- Keep first-person voice and personal narrative style.
- Keep emotional honesty about loving code while preferring higher shipping velocity.
- Do not include coworker names or direct transcript quotations in final post.
- Keep details anonymized and safe for public publishing.

## Working Brief (Agent Maintained)

- Audience: working software engineers (mid to senior), especially skeptics and partial adopters.
- Core thesis: this is not another tool upgrade; it is a workflow phase shift from individual code production to agent-directed execution.
- Primary example(s): personal 20+ year arc, current month of near-total agent-driven execution, transcript-derived practices.
- Potential title options:
  - "My New Reality of Software Engineering"
  - "From Writing Code to Directing Agents"
  - "The Phase Shift in Software Engineering"

## Proposed Outline (Agent Maintained)

1. A career that felt stable for 20 years
2. The phase shift: what changed in the last year
3. My workflow now: what I delegate vs what I own
4. The emotional tradeoff: craft vs shipping
5. Why this is coming for everyone (unevenly, but quickly)
6. How to adopt it safely and effectively
7. New bottlenecks and what to optimize next
8. Practical close: experiment now, before you are forced to

## Interview Notes (Agent + Author)

- Candidate pull-quote: "You might still own the solution, but you no longer have to type every step of it."
- Candidate concise framing line for early section: "For twenty years, software changed around me. This year, the job itself changed."
- Add one sentence about confidence calibration: how often outputs are wrong now and how you catch/fix them.
- Decide if naming specific model versions helps credibility or distracts from the larger point.

## Decision Log

- YYYY-MM-DD: Initial rough draft created.
- 2026-02-21: Organized rough draft into theme buckets, candidate sections, and extracted guidance from transcript.

## Next Session Starting Prompt

Use this prompt when resuming work with an agent:

"Read this rough draft file, ask me focused questions to fill any gaps, suggest 2-3 outline improvements, then draft/update `_drafts/YYYY-MM-DD-slug.md` while preserving my writing voice."
