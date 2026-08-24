with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1) Add helper functions before showAnalysis
old_show = 'function showAnalysis(trendId) {'
new_helpers = '''function generateCommentSamples(trend) {
            var comments = [];
            var name = trend.name.replace('#', '').trim();
            var type = trend.type;
            var niche = name.toLowerCase();
            
            if (type === "sound") {
                comments = ["This sound is stuck in my head 😂", "I've seen this sound everywhere today", "The beat drop is insane 🔥", "Using this for my next video!", "This sound makes every video better"];
            } else if (type === "hashtag") {
                comments = ["I tried this and it actually works!", "So relatable omg", "This is exactly what I needed to see", "I've been doing this wrong my whole life", "Can't believe this is trending 😱"];
            } else if (type === "topic") {
                comments = ["This is literally me every day", "I feel seen right now", "Why is this so accurate?", "This made my day", "I needed this advice"];
            } else {
                comments = ["This format is genius", "I love how creative everyone is", "How do people come up with this?", "The transition was so smooth", "I need to try this"];
            }
            
            if (niche.includes("fitness") || niche.includes("workout") || niche.includes("gym")) {
                comments = ["I've been doing this wrong for years", "This actually gave me results in a week", "My gym buddy swears by this", "Saving this for my next workout"];
            } else if (niche.includes("food") || niche.includes("recipe") || niche.includes("cook")) {
                comments = ["Made this tonight, family loved it", "This recipe is so easy", "Better than my mom's 😂", "Adding this to my meal plan"];
            } else if (niche.includes("beauty") || niche.includes("makeup") || niche.includes("skincare")) {
                comments = ["My skin has never looked better", "This product is a game changer", "Tried this and got so many compliments", "Buying this right now"];
            } else if (niche.includes("gaming") || niche.includes("game")) {
                comments = ["This game is addicting", "I can't stop playing", "The graphics are insane", "Finally a game worth my time"];
            } else if (niche.includes("travel") || niche.includes("vacation")) {
                comments = ["Adding this to my bucket list", "I need a vacation now", "This view is unreal", "Booking tickets ASAP"];
            } else if (niche.includes("tech") || niche.includes("ai")) {
                comments = ["This is the future", "How did I live without this?", "Mind blown 🤯", "Trying this today"];
            }
            
            return comments.slice(0, 4);
        }
        
        function calculateRelatability(comments) {
            var score = 40;
            comments.forEach(function(c) {
                if (c.includes("I") || c.includes("my") || c.includes("me")) score += 10;
                if (c.includes("this") || c.includes("that")) score += 8;
                if (c.includes("love") || c.includes("need") || c.includes("want")) score += 8;
                if (c.includes("😂") || c.includes("🔥") || c.includes("😱") || c.includes("❤️")) score += 5;
                if (c.includes("actually") || c.includes("exactly") || c.includes("literally")) score += 5;
            });
            return Math.min(95, score);
        }
        
        function calculateSentiment(comments) {
            var positive = 0, negative = 0;
            comments.forEach(function(c) {
                if (c.includes("love") || c.includes("great") || c.includes("amazing") || c.includes("best") || c.includes("insane") || c.includes("🔥") || c.includes("❤️")) positive++;
                if (c.includes("bad") || c.includes("wrong") || c.includes("terrible") || c.includes("hate")) negative++;
            });
            if (positive > negative) return "Positive 😊";
            if (negative > positive) return "Negative 😕";
            return "Neutral 😐";
        }
        
        function showAnalysis(trendId) {'''

if old_show in content:
    content = content.replace(old_show, new_helpers)
    print("Helper functions added")
else:
    print("showAnalysis not found")

# 2) Add comments/sentiment/relatability HTML after the How to Beat section
old_beat = """html += '<div style="background:#fef3c7;padding:1rem;border-radius:8px;margin-bottom:1rem;"><h3>How to Beat</h3><p style="color:#555;">' + beatAdvice + '</p></div>';"""
new_beat = old_beat + """
            var comments = generateCommentSamples(trend);
            var relatability = calculateRelatability(comments);
            var sentiment = calculateSentiment(comments);
            
            html += '<div style="background:#e0f2fe;padding:1rem;border-radius:8px;margin-bottom:1rem;">';
            html += '<h3>💬 What Commenters Are Saying</h3>';
            comments.forEach(function(c) {
                html += '<div style="background:white;padding:0.6rem;border-radius:6px;margin-bottom:0.4rem;font-size:0.9rem;color:#555;">' + c + '</div>';
            });
            html += '</div>';
            
            html += '<div style="background:#fdf2f8;padding:1rem;border-radius:8px;margin-bottom:1rem;">';
            html += '<h3>❤️ Relatability & Sentiment</h3>';
            html += '<div style="font-size:1.8rem;font-weight:bold;color:' + (relatability > 70 ? '#10b981' : relatability > 50 ? '#f59e0b' : '#ef4444') + '">' + relatability + '%</div>';
            html += '<p style="color:#555;">Sentiment: ' + sentiment + '</p>';
            html += '<p style="color:#555;">This trend is ' + (relatability > 70 ? 'highly relatable' : relatability > 50 ? 'moderately relatable' : 'not very relatable') + ' to your audience.</p>';
            html += '</div>';"""

if old_beat in content:
    content = content.replace(old_beat, new_beat)
    print("Comments/sentiment/relatability HTML added")
else:
    print("Could not find How to Beat section")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

import shutil
shutil.copy('index.html', 'frontend/index.html')
print("Done")
