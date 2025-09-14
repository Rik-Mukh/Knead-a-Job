# backend/job_tracker/services/match.py

from __future__ import annotations

import re
from typing import Dict, List, Tuple

from django.db.models import Q

from ..models import ResumeTemplate, Experience, Project, Education

try:
    # scikit-learn (ensure scikit-learn is in requirements.txt)
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except Exception as e:
    raise ImportError(
        "scikit-learn is required for match scoring. "
        "Add `scikit-learn>=1.3` to backend/requirements.txt and pip install."
    ) from e


# --- Basic normalization helpers ------------------------------------------------

_PUNCT_RE = re.compile(r"[^\w\s\-+/&]")  # keep word chars, whitespace, and a few symbols
_WS_RE = re.compile(r"\s+")

# Minimal combined English/Spanish stopwords for JD parsing. Feel free to expand.
_STOPWORDS = set(map(str.lower, """
a about above after again against all am an and any are aren't as at
be because been before being below between both but by
can can't cannot could couldn't
did didn't do does doesn't doing don't down during
each few for from further
had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself his how how's
i i'd i'll i'm i've if in into is isn't it it's its itself
let's me more most mustn't my myself
no nor not of off on once only or other ought our ours ourselves out over own
same shan't she she'd she'll she's should shouldn't so some such
than that that's the their theirs them themselves then there there's these they they'd they'll they're they've this those through to too
under until up very was wasn't we we'd we'll we're we've were weren't what what's when when's where where's which while who who's whom why why's with won't would wouldn't
ya y al algo alguna algunas alguno algunos ante antes como con contra cual cuales cuando de del desde donde dos el él ella ellas ellos en entre era erais eramos eran es esa esas ese esos esta estaba estabais estabamos estaban estado estais estamos estan estar está este esto estos fue fuera fueron fui fuimos ha habeis había habíais habíamos habían han hasta hay la las le les lo los mas más me mí mi mia mía mías mio mío míos mis mucha muchas mucho muchos muy nada ni no nos nosotras nosotros nuestra nuestras nuestro nuestros o os otra otras otro otros para pero poco por porque que quien quién quienes se sea segun según ser si sí sido sin sino somos son soy su sus también tampoco te ti tiene tienen toda todas todo todos tú tus tuya tuyas tuyo tuyos un una uno unos usted ustedes
""".split()))


def _normalize(text: str) -> str:
    """Lowercase, strip punctuation (mostly), collapse whitespace."""
    if not text:
        return ""
    text = text.lower()
    text = _PUNCT_RE.sub(" ", text)
    text = _WS_RE.sub(" ", text).strip()
    return text


def _strip_stopwords(tokens: List[str]) -> List[str]:
    return [t for t in tokens if t and t not in _STOPWORDS and not t.isdigit()]


def _tokenize(text: str) -> List[str]:
    return _strip_stopwords(_normalize(text).split())


def _parse_skills(skills_text: str) -> List[str]:
    """
    Parse skills from text, supporting multiple formats:
    - Colon-separated: "JavaScript: Python: React: Node.js"
    - Comma-separated: "JavaScript, Python, React, Node.js"
    - Line-separated: "JavaScript\nPython\nReact\nNode.js"
    - Structured format: "Languages: Python, Java, JavaScript\nFrameworks: React, Django"
    - Mixed formats
    """
    if not skills_text or not skills_text.strip():
        return []
    
    # First, handle structured format with category prefixes
    lines = skills_text.strip().split('\n')
    all_skills = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if line has a category prefix (e.g., "Languages:", "Frameworks:")
        if ':' in line:
            # Split on first colon to separate category from skills
            parts = line.split(':', 1)
            if len(parts) == 2:
                category, skills_part = parts
                category = category.strip().lower()
                skills_part = skills_part.strip()
                
                # Only process if it looks like a skills category
                if any(keyword in category for keyword in ['language', 'framework', 'library', 'tool', 'technology', 'skill']):
                    # Parse the skills part
                    skills_in_category = _parse_skills_list(skills_part)
                    all_skills.extend(skills_in_category)
                    continue
        
        # If no category prefix, treat the whole line as skills
        skills_in_line = _parse_skills_list(line)
        all_skills.extend(skills_in_line)
    
    # Remove duplicates while preserving order
    unique_skills = []
    seen = set()
    for skill in all_skills:
        if skill.lower() not in seen:
            unique_skills.append(skill)
            seen.add(skill.lower())
    
    return unique_skills


def _parse_skills_list(skills_text: str) -> List[str]:
    """
    Parse a simple list of skills separated by commas, colons, or semicolons.
    """
    if not skills_text or not skills_text.strip():
        return []
    
    # Split by common delimiters and clean up
    skills = []
    for delimiter in [':', ',', ';']:
        parts = skills_text.split(delimiter)
        for part in parts:
            cleaned = part.strip()
            # Skip very short or invalid terms
            if len(cleaned) < 2 or cleaned.lower() in ['on', 'to', 'in', 'of', 'and', 'or']:
                continue
            # Remove common prefixes/suffixes but be more careful
            if cleaned.endswith('JS') and len(cleaned) > 2:
                # Keep ReactJS, NodeJS, NextJS as they are meaningful
                pass
            elif cleaned == 'JS':
                continue  # Skip standalone JS
                
            if cleaned and cleaned not in skills:
                skills.append(cleaned)
    
    return skills


def _expand_skill_terms(skill: str) -> List[str]:
    """
    Expand a skill into multiple related terms for better matching.
    This helps catch variations and related technologies.
    """
    skill_lower = skill.lower().strip()
    expansions = [skill_lower]
    
    # Common skill expansions
    skill_expansions = {
        'js': ['javascript'],
        'javascript': ['js'],
        'react': ['reactjs', 'react.js', 'reactjs'],
        'reactjs': ['react', 'react.js'],
        'react.js': ['react', 'reactjs'],
        'nextjs': ['next.js', 'next'],
        'next.js': ['nextjs', 'next'],
        'next': ['nextjs', 'next.js'],
        'node': ['nodejs', 'node.js'],
        'nodejs': ['node', 'node.js'],
        'node.js': ['node', 'nodejs'],
        'html': ['html5'],
        'html5': ['html'],
        'css': ['css3'],
        'css3': ['css'],
        'sql': ['mysql', 'postgresql', 'postgres'],
        'mysql': ['sql'],
        'postgresql': ['sql', 'postgres'],
        'postgres': ['sql', 'postgresql'],
        'git': ['github', 'gitlab'],
        'github': ['git'],
        'gitlab': ['git'],
        'aws': ['amazon web services'],
        'amazon web services': ['aws'],
        'azure': ['microsoft azure'],
        'microsoft azure': ['azure'],
        'gcp': ['google cloud platform', 'google cloud'],
        'google cloud platform': ['gcp', 'google cloud'],
        'google cloud': ['gcp', 'google cloud platform'],
        'mongodb': ['mongo'],
        'mongo': ['mongodb'],
        'typescript': ['ts'],
        'ts': ['typescript'],
        'django': ['django framework'],
        'flask': ['flask framework'],
        'database': ['databases', 'database', 'db'],
        'intern': ['internship', 'intern', 'interning', 'internships'],
    }
    
    if skill_lower in skill_expansions:
        expansions.extend(skill_expansions[skill_lower])
    
    return list(set(expansions))  # Remove duplicates


# --- Data collection ------------------------------------------------------------

def _collect_resume_text(user) -> Tuple[str, List[str]]:
    """
    Build a single resume text blob + a token list from the current user's data.
    If your design is singleton (no per-user), we just take the first template.
    """
    # If you later move to per-user templates, filter by user: ResumeTemplate.objects.filter(user=user)...
    tmpl = ResumeTemplate.objects.first()

    parts: List[str] = []
    token_sources: List[str] = []  # fine-grained tokens for keyword diff

    if tmpl:
        # Handle basic fields
        for fld in ("name", "city", "email", "phone", "summary", "links"):
            val = getattr(tmpl, fld, "") or ""
            parts.append(val)
            token_sources.extend(_tokenize(val))
        
        # Handle skills with special parsing
        skills_text = getattr(tmpl, "skills", "") or ""
        if skills_text:
            # Parse skills using colon/comma/line separation
            parsed_skills = _parse_skills(skills_text)
            
            # Add skills to parts as both individual skills and expanded terms
            skills_for_parts = []
            for skill in parsed_skills:
                skills_for_parts.append(skill)
                # Add expanded skill terms for better matching
                expanded_terms = _expand_skill_terms(skill)
                skills_for_parts.extend(expanded_terms)
            
            # Add to parts and token sources
            skills_text_processed = " ".join(skills_for_parts)
            parts.append(skills_text_processed)
            token_sources.extend(_tokenize(skills_text_processed))

        # Experiences
        for exp in Experience.objects.all().order_by("-order", "-start_date"):
            seg = " ".join(filter(None, [
                exp.company, exp.position, exp.location or "",
                exp.description or ""
            ]))
            parts.append(seg)
            token_sources.extend(_tokenize(seg))

        # Projects
        for proj in Project.objects.all().order_by("-order", "-start_date"):
            seg = " ".join(filter(None, [
                proj.name, proj.description or "", proj.technologies or ""
            ]))
            parts.append(seg)
            token_sources.extend(_tokenize(seg))

        # Education
        for edu in Education.objects.all().order_by("-order", "-start_date"):
            seg = " ".join(filter(None, [
                edu.institution, edu.degree, edu.field_of_study or "", edu.location or ""
            ]))
            parts.append(seg)
            token_sources.extend(_tokenize(seg))

    resume_text = "\n".join(parts)
    return resume_text, token_sources


# --- Matching core --------------------------------------------------------------

def _tfidf_cosine(a: str, b: str) -> float:
    """
    Cosine similarity between two strings using TF-IDF (unigrams + bigrams).
    Returns 0..1.
    """
    if not a.strip() or not b.strip():
        return 0.0

    # Normalize both texts
    text_a = _normalize(a)
    text_b = _normalize(b)
    
    # If texts are too short, return 0
    if len(text_a.split()) < 5 or len(text_b.split()) < 5:
        return 0.0

    try:
        vectorizer = TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
            stop_words=None,  # we pre-clean; leaving as None preserves technical terms
        )
        X = vectorizer.fit_transform([text_a, text_b])
        
        # Check if we have valid vectors
        if X.shape[1] == 0:  # No vocabulary
            return 0.0
            
        sim = cosine_similarity(X[0:1], X[1:2])[0][0]
        
        # Clamp to [0,1] just in case of numerical noise
        return float(max(0.0, min(1.0, sim)))
        
    except Exception as e:
        # If there's any error in vectorization, return 0
        print(f"TF-IDF cosine similarity error: {e}")
        return 0.0


def _top_missing_keywords(resume_tokens: List[str], jd_text: str, top_k: int = 10) -> List[str]:
    """
    Find tokens/phrases that appear saliently in the JD but not (or barely) in the resume.
    Enhanced to better identify missing skills and technical terms.
    """
    jd_norm = _normalize(jd_text)
    jd_tokens = _tokenize(jd_norm)

    if not jd_tokens:
        return []

    # Create resume token set for faster lookup
    resume_set = set(resume_tokens)
    
    # Also create expanded resume set that includes skill expansions
    expanded_resume_set = set(resume_tokens)
    for token in resume_tokens:
        expanded_terms = _expand_skill_terms(token)
        expanded_resume_set.update(expanded_terms)

    # Use only unigrams (single words) for cleaner, more actionable keyword suggestions
    vectorizer = TfidfVectorizer(analyzer="word", ngram_range=(1, 1), min_df=1, max_features=1000, stop_words=None)
    # Fit on JD; transform on JD as a single document
    X = vectorizer.fit_transform([" ".join(jd_tokens)])
    vocab = vectorizer.get_feature_names_out()
    weights = X.toarray()[0]

    # Extended stopwords for better filtering
    extended_stopwords = _STOPWORDS | {
        'you', 'work', 'experience', 'use', 'allowance', 'end', 'interested', 'working',
        'have', 'will', 'are', 'can', 'should', 'would', 'could', 'may', 'might',
        'this', 'that', 'these', 'those', 'your', 'our', 'their', 'company',
        'team', 'role', 'position', 'job', 'career', 'opportunity', 'environment',
        'fast', 'paced', 'high', 'growth', 'startup', 'scaleup', 'dynamic',
        'looking', 'hire', 'join', 'build', 'create', 'develop', 'design',
        'problem', 'solution', 'challenge', 'project', 'feature', 'service',
        'aim', 'supercharge', 'requests', 'handles', 'ingest', 'process', 'maintaining',
        'ship', 'meaningfully', 'propel', 'forward', 'recognize', 'impact',
        'own', 'including', 'deployment', 'monitoring', 'got', 'per',
        'write', 'production', 'ready', 'well', 'tested', 'code', 'first', 'week',
        'driven', 'close', 'customer', 'performing', 'experiments', 'nearly',
        'everything', 'launch', 'combination', 'across', 'multiple', 'services',
        'codebases', 'state', 'art', 'powered', 'primarily', 'written', 'frontend',
        'storage', 'caching', 'version', 'control', 'infrastructure', 'hosted',
        'takes', 'under', 'minutes', 'merged', 'reach', 'invest', 'heavily',
        'automated', 'alerting', 'using', 'datadog', 'amplitude', 'client', 'side',
        'metrics', 'experimentation', 'snowflake', 'warehouse', 'least', 'months',
        'web', 'development', 'preferably', 'exposure', 'modern', 'framework',
        'servers', 'learn', 'quickly', 'regardless', 'languages', 'technologies',
        'taking', 'ownership', 'shipping', 'entire', 'features', 'thrive', 'decoding',
        'intricate', 'problems', 'logical', 'well', 'reasoned', 'solutions',
        'help', 'lives', 'maximize', 'started', 'engineering', 'interns', 'software',
        'both', 'employees', 'customers', 'everyone', 'experience', 'offer',
        'promise', 'opportunity', 'unlock', 'potential', 'learning', 'celebrated',
        'realized', 'more', 'than', 'fast', 'paced', 'high', 'growth', 'tech',
        'care', 'people', 'take', 'seriously', 'career', 'progression', 'ubereats', 'alignment',
        'aspects', 'available', 'compensation', 'components', 'data', 'pay', 'based', 'direct',
        'business', 'challenging', 'completed', 'day', 'equal', 'great', 'number', 'used', 'one',
        'past', 'our', 'work', 'use', 'development', 'projects', 'structured', 'understanding',
        'policies', 'process', 'systems', 'tools', 'platforms', 'technologies', 'architecture',
        'successfully', 'structure', 'talent', 'talented', 'levels', 'utilize', 'resources', 'prior',
        'term', 'terms', 'techincality'
    }
    
    # Score terms and filter out those already well-covered in resume tokens
    scored = []
    for term, w in zip(vocab, weights):
        # exclude trivial terms and common words
        if (term in extended_stopwords or 
            term.isdigit() or 
            len(term) < 3 or  # Minimum 3 characters
            any(common in term for common in ['you', 'work', 'experience', 'use', 'allowance', 'interested'])):
            continue
        
        # Check if term is already present (including expanded forms)
        if term in expanded_resume_set:
            continue
            
        # Boost score for common technical terms and skills
        technical_boost = 1.0
        technical_keywords = [
            'javascript', 'python', 'java', 'react', 'reactjs', 'angular', 'vue', 'node', 'nodejs', 'sql',
            'html', 'css', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'github', 'gitlab',
            'api', 'rest', 'graphql', 'database', 'frontend', 'backend', 'fullstack', 'full-stack',
            'machine learning', 'ai', 'data science', 'analytics', 'agile', 'scrum',
            'typescript', 'ts', 'php', 'ruby', 'go', 'rust', 'django', 'flask', 'express',
            'mongodb', 'mongo', 'mysql', 'postgresql', 'postgres', 'redis', 'elasticsearch',
            'jenkins', 'ci/cd', 'cicd', 'terraform', 'ansible', 'linux', 'fastapi', 'microservices',
            'testing', 'debugging', 'monitoring', 'deployment', 'production', 'infrastructure',
            'architecture', 'performance', 'scalability', 'security', 'authentication',
            'authorization', 'optimization', 'integration', 'automation', 'containerization'
        ]
        
        if any(keyword in term for keyword in technical_keywords):
            technical_boost = 3.0  # Much higher boost for technical terms
        elif any(domain in term for domain in [
            'web', 'mobile', 'cloud', 'devops', 'fullstack', 'backend', 'frontend',
            'database', 'server', 'client', 'framework', 'library', 'tool'
        ]):
            technical_boost = 2.0  # Medium boost for domain terms
        
        scored.append((term, float(w) * technical_boost))

    # Sort by weight desc, return top_k unique terms
    scored.sort(key=lambda t: t[1], reverse=True)
    out: List[str] = []
    seen = set()
    
    for term, weight in scored:
        if term not in seen:
            # Additional filtering for quality terms
            if (len(term) >= 3 and  # Minimum length
                not any(bad in term for bad in ['you', 'work', 'experience', 'use', 'allowance', 'interested']) and
                not term.isdigit() and
                term not in extended_stopwords
            ):
                out.append(term)
                seen.add(term)
        if len(out) >= top_k:
            break
    
    # If we don't have enough quality terms, try to get some meaningful ones
    if len(out) < 3:
        # Look for any remaining meaningful terms
        for term, weight in scored:
            if (term not in seen and 
                len(term) >= 3 and 
                not term.isdigit() and
                not any(bad in term for bad in ['you', 'work', 'experience', 'use', 'allowance'])):
                out.append(term)
                seen.add(term)
            if len(out) >= top_k:
                break
    
    return out


# --- Public API -----------------------------------------------------------------

def _analyze_skills_match(user, jd_text: str) -> Dict:
    """
    Analyze skills match specifically between resume skills and job description.
    Returns insights about skills coverage and missing skills.
    """
    tmpl = ResumeTemplate.objects.first()
    if not tmpl or not tmpl.skills:
        return {
            "skills_found": [],
            "skills_missing": [],
            "skills_coverage": 0.0,
            "total_skills_mentioned": 0
        }
    
    # Parse resume skills
    resume_skills = _parse_skills(tmpl.skills)
    resume_skills_lower = [skill.lower().strip() for skill in resume_skills]
    
    # Normalize job description and extract potential skills
    jd_norm = _normalize(jd_text)
    jd_tokens = _tokenize(jd_norm)
    
    # Common technical skills to look for in job description
    technical_skills = [
        'javascript', 'python', 'java', 'react', 'reactjs', 'angular', 'vue', 'node', 'nodejs', 'sql',
        'html', 'css', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'github', 'gitlab',
        'api', 'rest', 'graphql', 'database', 'frontend', 'backend', 'fullstack', 'full-stack',
        'machine learning', 'ai', 'data science', 'analytics', 'agile', 'scrum',
        'typescript', 'ts', 'php', 'ruby', 'go', 'rust', 'c++', 'c#', '.net', 'spring',
        'django', 'flask', 'express', 'mongodb', 'mongo', 'mysql', 'postgresql', 'postgres', 'redis',
        'elasticsearch', 'jenkins', 'ci/cd', 'cicd', 'terraform', 'ansible', 'linux',
        'unix', 'bash', 'powershell', 'figma', 'sketch', 'adobe', 'photoshop',
        'nextjs', 'next.js', 'fastapi', 'microservices'
    ]
    
    # Find skills mentioned in job description
    jd_skills_found = []
    for skill in technical_skills:
        if skill in jd_tokens:
            jd_skills_found.append(skill)
    
    # Find which of these skills are in the resume
    skills_found = []
    skills_missing = []
    
    for jd_skill in jd_skills_found:
        found = False
        # Check direct match
        if jd_skill in resume_skills_lower:
            found = True
        else:
            # Check expanded forms and partial matches
            for resume_skill in resume_skills:
                resume_skill_lower = resume_skill.lower()
                expanded_terms = _expand_skill_terms(resume_skill)
                expanded_terms_lower = [term.lower() for term in expanded_terms]
                
                # Direct expansion match
                if jd_skill in expanded_terms_lower:
                    found = True
                    break
                
                # Partial match (e.g., "react" matches "reactjs")
                if jd_skill in resume_skill_lower or resume_skill_lower in jd_skill:
                    found = True
                    break
                
                # Check if any expanded term matches
                if any(term in jd_skill or jd_skill in term for term in expanded_terms_lower):
                    found = True
                    break
        
        if found:
            skills_found.append(jd_skill)
        else:
            skills_missing.append(jd_skill)
    
    # Calculate coverage
    total_skills = len(jd_skills_found)
    skills_coverage = len(skills_found) / total_skills if total_skills > 0 else 0.0
    
    return {
        "skills_found": skills_found,
        "skills_missing": skills_missing,
        "skills_coverage": round(skills_coverage, 4),
        "total_skills_mentioned": total_skills
    }


def compute_match_score(user, jd_text: str, *, top_k: int = 10) -> Dict:
    """
    Build a resume corpus from DB, compare to the provided JD text, and return:
      {
        "score": float in [0,1],
        "missing_keywords": [str, ...],
        "skills_analysis": {
          "skills_found": [str, ...],
          "skills_missing": [str, ...],
          "skills_coverage": float,
          "total_skills_mentioned": int
        }
      }
    """
    resume_text, resume_tokens = _collect_resume_text(user=user)

    # Calculate TF-IDF cosine similarity
    tfidf_score = _tfidf_cosine(resume_text, jd_text)
    
    # Get skills analysis
    skills_analysis = _analyze_skills_match(user, jd_text)
    
    # If TF-IDF score is very low but skills coverage is high, use a hybrid score
    if tfidf_score < 0.1 and skills_analysis["skills_coverage"] > 0.5:
        # Base score on skills coverage with some bonus for TF-IDF
        skills_based_score = skills_analysis["skills_coverage"] * 0.8  # Skills weight
        tfidf_bonus = tfidf_score * 0.2  # Small bonus from TF-IDF
        final_score = skills_based_score + tfidf_bonus
    else:
        # Use TF-IDF score as primary, but give some boost for good skills coverage
        final_score = tfidf_score
        if skills_analysis["skills_coverage"] > 0.7:
            final_score = min(1.0, tfidf_score + 0.1)  # Small boost for good skills coverage
    
    missing = _top_missing_keywords(resume_tokens, jd_text, top_k=top_k)

    return {
        "score": round(final_score, 4),
        "missing_keywords": missing,
        "skills_analysis": skills_analysis,
    }
